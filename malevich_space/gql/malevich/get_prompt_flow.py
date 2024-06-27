from gql import gql


get_flow = gql(
    """
    query GetFlow($flow_id: String!) {
      flow(uid: $flow_id) {
        details {
          uid
        }
        inFlowComponents {
          edges {
            rel {
              versionId
            }
            node {
              prev {
                edges {
                  node {
                    details {
                      uid
                    }
                  }
                }
              }
              details {
                uid
                alias
              }
              component {
                details {
                  uid
                  reverseId
                }
              }
                  cfg {
                    details {
                      uid
                      coreId
                      coreName
                      cfgJson
                      readableName
                    }
                  }
              app {
                details {
                  uid
                }
                op(opType: ["input", "processor", "output"]) {
                  edges {
                    node {
                      details {
                        uid
                        name
                      }
                    }
                  }
                }
              }
              collectionAlias {
                details {
                  uid
                }
              }
              flow {
                details {
                  uid
                }
              }
            }
          }
        }
      }
    }
    """
)
