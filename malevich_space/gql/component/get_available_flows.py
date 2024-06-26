
from gql import gql

get_available_flows = gql("""
query GetAvailableFlows($reverse_id: String!) {
  component(reverseId: $reverse_id) {
    branches {
      edges {
        node {
          versions {
            edges {
              node {
                details {
                  uid
                  readableName
                }
                flow {
                  details {
                    uid
                  }
                }
              }
            }
          }
          details {
            uid
            name
          }
          activeVersion {
            flow {
                details {
                    uid
                }
            }
          }
        }
      }
    }
    activeBranch {
      details {
        uid
      }
    }
  }
}
""")