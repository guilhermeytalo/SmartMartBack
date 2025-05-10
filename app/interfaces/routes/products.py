import csv
import os
from io import StringIO

from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.infrastructure.db.database import get_db
from app.infrastructure.db.models.category import CategoryModel
from app.infrastructure.db.models.product import ProductModel
from app.interfaces.dtos.product_dto import ProductCreateDTO, ProductResponseDTO, CategoryResponseDTO

router = APIRouter(tags=["Products"])


@router.post("/products", response_model=ProductResponseDTO)
def create_product(
        product_data: ProductCreateDTO,
        db: Session = Depends(get_db)
):
    if isinstance(product_data.category, CategoryResponseDTO):

        if product_data.category.id:
            category = db.query(CategoryModel).get(product_data.category.id)
        else:
            category = db.query(CategoryModel).filter_by(
                name=product_data.category.name
            ).first()

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found. Provide a valid ID/name or create a new one."
            )
    else:

        existing_category = db.query(CategoryModel).filter_by(
            name=product_data.category.name
        ).first()

        if existing_category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Category '{product_data.category.name}' already exists."
            )

        category = CategoryModel(**product_data.category.model_dump())
        db.add(category)
        db.flush()

    product = ProductModel(
        **product_data.model_dump(exclude={"category"}),
        category_id=category.id
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    return product


@router.get("/products", response_model=list[ProductResponseDTO])
def get_all_products(db: Session = Depends(get_db)):
    from app.application.use_cases.list_products import list_products
    return list_products(db)


@router.post("/products/import-csv", status_code=201)
def import_products_from_csv(
        file: UploadFile = File(...),
        db: Session = Depends(get_db)
):
    """
    Import products from a CSV file.

    CSV format expected:
    id,name,description,price,category_id,brand,quantity

    Category handling rules:
    - If the category_id exists, it will use that category
    - If the category_id doesn't exist but a category with the same name exists, it will return an error with the correct ID
    - If the category_id doesn't exist and no category with that name exists, it will create a new category
    - Prevents creating multiple categories with the same name
    """
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="File must be a CSV.")

    try:
        content = file.file.read().decode("utf-8")
        csv_reader = csv.DictReader(StringIO(content))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading CSV: {str(e)}")

    products_to_create = []

    existing_categories = {
        cat.id: cat for cat in db.query(CategoryModel).all()
    }

    category_names_to_id = {
        cat.name.lower(): cat.id for cat in existing_categories.values()
    }

    for idx, row in enumerate(csv_reader, start=1):
        try:
            for field in ["name", "price", "brand"]:
                if field not in row or not row[field]:
                    return {"detail": f"Row {idx}: Missing required field '{field}'"}

            category_id_str = row.get("category_id")
            category_name = row.get("category_name")

            if not category_id_str:
                return {"detail": f"Row {idx}: Missing required field 'category_id'"}

            try:
                category_id = int(category_id_str)
            except ValueError:
                return {"detail": f"Row {idx}: Invalid category_id format '{category_id_str}'"}

            if category_id in existing_categories:
                category = existing_categories[category_id]

                if category_name and category.name.lower() != category_name.lower():
                    return {
                        "detail": f"Row {idx}: Category ID/name mismatch. ID {category_id} belongs to '{category.name}', not '{category_name}'."
                    }
            else:

                if category_name and category_name.lower() in category_names_to_id:
                    existing_id = category_names_to_id[category_name.lower()]
                    return {
                        "detail": f"Row {idx}: Cannot create category with ID {category_id} and name '{category_name}'. A category with this name already exists with ID {existing_id}."
                    }

                if not category_name:
                    return {
                        "detail": f"Row {idx}: Category ID {category_id} not found. Please provide a category name to create it."
                    }

                new_category = CategoryModel(id=category_id, name=category_name)
                db.add(new_category)
                db.flush()

                existing_categories[category_id] = new_category
                category_names_to_id[category_name.lower()] = category_id

                category = new_category

            try:
                product = ProductModel(
                    name=row["name"],
                    description=row.get("description", ""),
                    price=float(row["price"]),
                    brand=row["brand"],
                    quantity=int(row.get("quantity", 0)),
                    category_id=category.id
                )
                products_to_create.append(product)
            except ValueError as e:
                return {"detail": f"Row {idx}: Invalid data format - {str(e)}"}

        except Exception as e:
            return {"detail": f"Row {idx}: Unexpected error - {str(e)}"}

    if not products_to_create:
        return {"detail": "No valid products found in CSV."}

    try:
        db.bulk_save_objects(products_to_create)
        db.commit()
        return {"message": f"Successfully imported {len(products_to_create)} products."}
    except Exception as e:
        db.rollback()
        return {"detail": f"Database error: {str(e)}"}

@router.get("/products/sample-csv", response_class=FileResponse)
def download_sample_csv():
    sample_path = os.path.join("static", "sample_products.csv")
    return FileResponse(
        path=sample_path,
        media_type="text/csv",
        filename="sample_products.csv"
    )
