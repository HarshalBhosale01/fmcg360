from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("smoke-test").master("local[*]").getOrCreate()

data = [("SKU001", "Cola 500ml", 40), ("SKU002", "Salted Chips 50g", 20)]
df = spark.createDataFrame(data, ["product_id", "product_name", "price"])

df.show()
print("Row count:", df.count())

spark.stop()
