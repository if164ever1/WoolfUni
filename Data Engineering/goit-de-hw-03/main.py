from pathlib import Path
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import IntegerType, LongType, DoubleType

BASE_DIR = Path(__file__).resolve().parent

spark = SparkSession.builder.appName('GoIT-DE-HW-03').master('local[*]').getOrCreate()

try:
    # 1. Load CSV files into separate DataFrames.
    users = spark.read.option('header', True).option('inferSchema', True).csv(str(BASE_DIR / 'users.csv'))
    purchases = spark.read.option('header', True).option('inferSchema', True).csv(str(BASE_DIR / 'purchases.csv'))
    products = spark.read.option('header', True).option('inferSchema', True).csv(str(BASE_DIR / 'products.csv'))

    print('\nSTEP 1: Original DataFrames')
    users.show(10, truncate=False)
    purchases.show(10, truncate=False)
    products.show(10, truncate=False)

    # 2. Remove rows containing any null values, including nulls after casting.
    users_clean = users.withColumn('user_id', F.col('user_id').cast(LongType())) \
        .withColumn('age', F.col('age').cast(IntegerType())).na.drop()
    purchases_clean = purchases.withColumn('user_id', F.col('user_id').cast(LongType())) \
        .withColumn('product_id', F.col('product_id').cast(LongType())) \
        .withColumn('quantity', F.col('quantity').cast(DoubleType())).na.drop()
    products_clean = products.withColumn('product_id', F.col('product_id').cast(LongType())) \
        .withColumn('price', F.col('price').cast(DoubleType())).na.drop()

    print('\nSTEP 2: Clean DataFrames')
    users_clean.show(10, truncate=False)
    purchases_clean.show(10, truncate=False)
    products_clean.show(10, truncate=False)

    purchase_details = purchases_clean.join(products_clean, on='product_id', how='inner') \
        .withColumn('amount', F.col('quantity') * F.col('price'))

    # 3. Total purchases by product category (all ages).
    category_totals = purchase_details.groupBy('category').agg(
        F.round(F.sum('amount'), 2).alias('total_amount')
    ).orderBy(F.desc('total_amount'))
    print('\nSTEP 3: Total amount by category')
    category_totals.show(truncate=False)

    # 4. Total purchases by category for users aged 18–25 inclusive.
    young_users = users_clean.filter(F.col('age').between(18, 25)).select('user_id')
    young_purchases = purchase_details.join(young_users, on='user_id', how='inner')
    young_category_totals = young_purchases.groupBy('category').agg(
        F.sum('amount').alias('total_amount')
    )
    print('\nSTEP 4: Amount by category, ages 18–25')
    young_category_totals.select('category', F.round('total_amount', 2).alias('total_amount')) \
        .orderBy(F.desc('total_amount')).show(truncate=False)

    # 5. Percentage of total spending for ages 18–25 by category.
    # Window without partition covers all categories, not each category separately.
    from pyspark.sql.window import Window
    percentages = young_category_totals.withColumn(
        'overall_amount', F.sum('total_amount').over(Window.partitionBy())
    ).withColumn(
        'percentage',
        F.when(F.col('overall_amount') > 0,
               F.round(F.col('total_amount') / F.col('overall_amount') * 100, 2))
         .otherwise(F.lit(0.0))
    ).select('category', F.round('total_amount', 2).alias('total_amount'), 'percentage') \
        .orderBy(F.desc('percentage'), F.asc('category'))
    print('\nSTEP 5: Spending percentage by category, ages 18–25')
    percentages.show(truncate=False)

    # 6. Top 3 categories by spending percentage.
    top_three = percentages.limit(3)
    print('\nSTEP 6: Top 3 categories')
    top_three.show(truncate=False)
finally:
    spark.stop()
