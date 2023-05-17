from celery import shared_task
import pandas as pd

from products.models import Product, Category, SubCategory
from users.models import User

@shared_task
def load_products(user_pk):
    user = User.objects.get(pk=user_pk)
    df = pd.read_csv('products.csv')
    products_names = Product.objects.values_list('name', flat=True)
    products_to_create = []
    for i in range(len(df)):
        if not all(
            [
                not pd.isna(df.iloc[i]['Product Name']),
                not pd.isna(df.iloc[i]['Uniq Id']),
                not pd.isna(df.iloc[i]['Selling Price']),
                not pd.isna(df.iloc[i]['About Product']),
                not pd.isna(df.iloc[i]['Category']),
            ]):
            continue # skip this row if any of the above field is empty

        if df.iloc[i]['Product Name'] in products_names:
            print('product already exists ', df.iloc[i]['Product Name'])
            continue

        try:
            price = float(df.iloc[i]['Selling Price'].replace('$', '').split(' ')[0])
        except:
            continue

        category = Category.objects.get_or_create(name=df.iloc[i]['Category'].replace(' | ', '|').split('|')[0])[0]
        subcategory = SubCategory.objects.get_or_create(name=df.iloc[i]['Category'].replace(' | ', '|').split('|')[-1], category=category)[0]

        products_to_create.append(
            Product(
                name = df.iloc[i]['Product Name'],
                owner = user,
                SKU = df.iloc[i]['Uniq Id'],
                price = price,
                description = df.iloc[i]['About Product'],
                category = category,
                subcategory = subcategory,
                )
        )

    Product.objects.bulk_create(products_to_create)

    return f'products created {len(products_to_create)}'