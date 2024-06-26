from gql import gql


create_version = gql(
    """
    mutation CreateVersion(
        $branch_id: String!,
        $readable_name: String!,
        $branch_version_status: String!,
        $updates_markdown: String!,
        $commit_digest: String
    ) {
      branch(uid: $branch_id) {
        createVersion(
          input: {
            node: {
              readableName: $readable_name
              updatesMarkdown: $updates_markdown
              commitDigest: $commit_digest
            },
            rel: {
              status: $branch_version_status
            }
          }
        ) {
          uid
          readableName
        }
      }
    }
    """
)

get_version = gql(
    """
    query GetComponentByReverseID($version_id: String!) {
      version(uid: $version_id) {
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
    """
)