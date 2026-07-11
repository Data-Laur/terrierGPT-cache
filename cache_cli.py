#!/usr/bin/env python
"""
TerrierGPT Vector Database Cache CLI

Usage:
    python cache_cli.py cache --query "..." --response "..."
    python cache_cli.py query --query "..."
    python cache_cli.py stats
"""

import sys
import argparse
from embedding_pipeline import TerrierGPTCache


def main():
    parser = argparse.ArgumentParser(
        description="TerrierGPT Vector Database Cache CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Cache a response
  python cache_cli.py cache --query "Where is the sustainability office?" --response "685 Commonwealth Ave"
  
  # Query the cache
  python cache_cli.py query --query "Where can I find the sustainability office?"
  
  # Show cache stats
  python cache_cli.py stats
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Cache command
    cache_parser = subparsers.add_parser("cache", help="Cache a query-response pair")
    cache_parser.add_argument("--query", required=True, help="Query text to cache")
    cache_parser.add_argument("--response", required=True, help="Response text to cache")
    cache_parser.add_argument("--source", default="manual", help="Source metadata (default: manual)")

    # Query command
    query_parser = subparsers.add_parser("query", help="Query the cache")
    query_parser.add_argument("--query", required=True, help="Query text to search for")

    # Stats command
    stats_parser = subparsers.add_parser("stats", help="Show cache statistics")

    args = parser.parse_args()

    # Initialize cache
    cache = TerrierGPTCache(similarity_threshold=0.75)

    if args.command == "cache":
        doc_id = cache.cache_response(
            query=args.query,
            response=args.response,
            metadata={"source": args.source}
        )
        print(f"✅ Cached: {doc_id}")
        print(f"   Query: {args.query}")
        print(f"   Response: {args.response}")

    elif args.command == "query":
        result = cache.query_cache(args.query)
        if result:
            print(f"✅ Cache hit!")
            print(f"   Similarity: {result['similarity']:.6f}")
            print(f"   Response: {result['response']}")
            print(f"   Source: {result['metadata'].get('source', 'unknown')}")
        else:
            print(f"❌ No match in cache (below 0.75 threshold)")
            print(f"   Query: {args.query}")

    elif args.command == "stats":
        stats = cache.get_cache_stats()
        print("📊 Cache Statistics:")
        print(f"   Total cached: {stats['total_cached']}")
        print(f"   Threshold: {stats['threshold']}")
        print(f"   Model: {stats['model']}")

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
