from gql import gql


get_comp_with_reverse_id = gql(
    """
query GetComponentByReverseID($reverse_id: String, $uid: String) {
  component(reverseId: $reverse_id, uid: $uid) {
    details {
      uid
      name
      reverseId
      type
      descriptionMarkdown
    }
    activeBranch {
      details {
        uid
        name
        status
      }
    }
    activeBranchVersion {
      details {
        uid
        readableName
        updatesMarkdown
      }
      collection {
        details {
          uid
          coreId
        }
      }
      asset {
        details {
          uid
          corePath
        }
        downloadUrl
        uploadUrl
      }
      flow {
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
      app {
        details {
          uid
          containerRef
          containerUser
          containerToken
        }
        avCfg {
          edges {
            node {
              details {
                uid
                cfgJson
                coreName
                createdAt
                readableName
              }
            }
          }
        }
        avOp(opType: ["input", "processor", "output", "preinit"]) {
          edges {
            node {
              details {
                uid
                name
                coreId
                doc
                finishMsg
                tl
                query
                mode
                collectionsNames
                extraCollectionsNames
                collectionOutNames
                args {
                  argName
                  argType
                  argOrder
                }
              }
              deps {
                details {
                  uid
                  key
                  type
                }
              }
              inputSchema {
                details {
                  uid
                  coreId
                }
              }
              outputSchema {
                details {
                  uid
                  coreId
                }
              }
            }
            rel {
              type
            }
          }
        }
      }
    }
  }
}
    """
)
