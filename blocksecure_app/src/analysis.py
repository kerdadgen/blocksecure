from pymongo import MongoClient

def analyze_transactions_simple():
    """Analyzes transactions based on a simple rule (amount > threshold) and updates MongoDB."""
    try:
        client = MongoClient("mongodb://localhost:27017/")
        db = client["blocksecure_db"]
        transactions_collection = db["eth_transactions"]
        
        suspicious_threshold = 5000.0
        analysis_count = 0
        suspicious_count = 0

        print(f"Starting simple analysis with threshold: {suspicious_threshold}")

        # Reset previous analysis results (optional, depends on desired behavior)
        # transactions_collection.update_many({}, {"$set": {"is_suspicious": False, "analysis_notes": ""}})
        # print("Reset previous analysis results.")

        for tx in transactions_collection.find():
            analysis_count += 1
            is_suspicious = False
            analysis_notes = ""

            # Simple rule: amount > threshold
            if tx.get("amount", 0) > suspicious_threshold:
                is_suspicious = True
                analysis_notes = f"Suspicious: Amount ({tx.get('amount')}) exceeds threshold ({suspicious_threshold})."
                suspicious_count += 1
            
            # Update the document in MongoDB only if the status changed or notes were added
            if tx.get("is_suspicious") != is_suspicious or tx.get("analysis_notes") != analysis_notes:
                 transactions_collection.update_one(
                    {"_id": tx["_id"]},
                    {"$set": {"is_suspicious": is_suspicious, "analysis_notes": analysis_notes}}
                )

        print(f"Analysis complete. Analyzed {analysis_count} transactions. Found {suspicious_count} suspicious transactions.")
        client.close()
        return {"analyzed_count": analysis_count, "suspicious_count": suspicious_count}

    except Exception as e:
        print(f"An error occurred during analysis: {e}")
        return {"error": str(e)}

# Example usage (can be run independently for testing)
if __name__ == "__main__":
    result = analyze_transactions_simple()
    print(result)

