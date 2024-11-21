from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf
from pyspark.sql.types import StringType
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Initialize Spark session
spark = SparkSession.builder \
    .appName("SentimentAnalysis") \
    .getOrCreate()

# Reuse centralized sentiment analysis logic
def analyze_sentiment_vader(comment):
    """
    Analyze sentiment polarity using VADER.
    Return Positive, Negative, or Neutral based on compound score.
    """
    if not comment:
        return "Neutral"
    scores = analyzer.polarity_scores(comment)
    if scores['compound'] >= 0.05:
        return "Positive"
    elif scores['compound'] <= -0.05:
        return "Negative"
    else:
        return "Neutral"

# Register UDF for Spark
sentiment_udf = udf(analyze_sentiment_vader, StringType())

def process_sentiment(input_path, output_path):
    """
    Perform sentiment analysis on JSON data and save results to HDFS.
    
    Parameters:
    - input_path: Path to input JSON file (e.g., HDFS or local path).
    - output_path: Path to save output data (e.g., HDFS location).
    """
    # Read input JSON data
    df = spark.read.json(input_path)

    # Ensure 'comment' column exists
    if "comment" not in df.columns:
        raise ValueError("Input data must contain a 'comment' column")
    
    # Apply sentiment analysis
    df_with_sentiment = df.withColumn("sentiment", sentiment_udf(col("comment")))

    # Save results to output path in Parquet format
    df_with_sentiment.write.mode("overwrite").format("parquet").save(output_path)
    print(f"Sentiment analysis completed. Results saved to {output_path}")


if __name__ == "__main__":
    # Example input/output paths
    input_path = "hdfs://namenode:8020/input/comments.json"  # Input JSON file path
    output_path = "hdfs://namenode:8020/output/sentiment_analysis"  # Output HDFS path

    # Run sentiment analysis
    process_sentiment(input_path, output_path)
