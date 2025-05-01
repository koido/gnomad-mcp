#!/usr/bin/env python3
"""
Core logic for fetching and saving the gnomAD GraphQL schema (latest only).
This module is intended for programmatic use. For CLI, use gnomad/schema.py.
"""

import json
import logging
from pathlib import Path
import aiohttp
from datetime import datetime
import os

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# API endpoint (always latest schema)
API_URL = "https://gnomad.broadinstitute.org/api"

# GraphQL introspection query
INTROSPECTION_QUERY = """
query IntrospectionQuery {
  __schema {
    queryType {
      name
      fields {
        name
        description
        args {
          name
          description
          type {
            kind
            name
            ofType {
              kind
              name
              ofType {
                kind
                name
                ofType {
                  kind
                  name
                }
              }
            }
          }
          defaultValue
        }
        type {
          kind
          name
          ofType {
            kind
            name
            ofType {
              kind
              name
              ofType {
                kind
                name
              }
            }
          }
        }
      }
    }
    types {
      kind
      name
      description
      fields {
        name
        description
        args {
          name
          description
          type {
            kind
            name
            ofType {
              kind
              name
              ofType {
                kind
                name
                ofType {
                  kind
                  name
                }
              }
            }
          }
          defaultValue
        }
        type {
          kind
          name
          ofType {
            kind
            name
            ofType {
              kind
              name
              ofType {
                kind
                name
              }
            }
          }
        }
      }
      inputFields {
        name
        description
        type {
          kind
          name
          ofType {
            kind
            name
            ofType {
              kind
              name
              ofType {
                kind
                name
              }
            }
          }
        }
        defaultValue
      }
      interfaces {
        kind
        name
        ofType {
          kind
          name
          ofType {
            kind
            name
            ofType {
              kind
              name
            }
          }
        }
      }
      enumValues {
        name
        description
        isDeprecated
        deprecationReason
      }
      possibleTypes {
        kind
        name
        ofType {
          kind
          name
          ofType {
            kind
            name
            ofType {
              kind
              name
            }
          }
        }
      }
    }
    directives {
      name
      description
      locations
      args {
        name
        description
        type {
          kind
          name
          ofType {
            kind
            name
            ofType {
              kind
              name
              ofType {
                kind
                name
              }
            }
          }
        }
        defaultValue
      }
    }
  }
}
"""

async def fetch_schema():
    """
    Fetch the latest gnomAD schema from the API.
    Returns the schema dict and a metadata dict for logging.
    """
    fetch_time = datetime.now().isoformat()
    logger.info(f"Fetching latest schema from {API_URL} ...")
    headers = {'Content-Type': 'application/json'}
    introspection_payload = {"query": INTROSPECTION_QUERY}
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(
                API_URL,
                json=introspection_payload,
                headers=headers,
                ssl=True
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    logger.error(f"HTTP error: {response.status} - {error_text}")
                    return None, None
                result = await response.json()
                if 'errors' in result:
                    logger.error(f"GraphQL error: {result['errors']}")
                    return None, None
                schema = result.get('data', {})
                schema['metadata'] = {
                    'api_url': API_URL,
                    'fetched_at': fetch_time,
                    'request_payload': introspection_payload
                }
                log_metadata = {
                    'api_url': API_URL,
                    'fetched_at': fetch_time,
                    'request_payload': introspection_payload
                }
                return schema, log_metadata
        except aiohttp.ClientError as e:
            logger.error(f"HTTP communication error: {e}")
            return None, None
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return None, None

def save_schema(schema, output_dir="tests/input"):
    """
    Save the latest schema to a JSON file and write a log file with fetch details.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    fetch_time = datetime.now().isoformat()
    # File names (no version)
    output_path = output_dir / "gnomad_schema.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(schema, f, indent=2)
    logger.info(f"Schema saved to {output_path}")
    # Write log file
    log_path = output_dir / "gnomad_schema_fetch.log"
    log_data = {
        'api_url': API_URL,
        'fetched_at': schema.get('metadata', {}).get('fetched_at', fetch_time),
        'output_file': str(output_path)
    }
    if schema.get('metadata', {}).get('request_payload'):
        log_data['request_payload'] = schema['metadata']['request_payload']
    with open(log_path, 'w', encoding='utf-8') as logf:
        for k, v in log_data.items():
            if k == 'request_payload':
                logf.write(f"{k}: {json.dumps(v, ensure_ascii=False, indent=2)}\n")
            else:
                logf.write(f"{k}: {v}\n")
    logger.info(f"Fetch log saved to {log_path}")
    return output_path 