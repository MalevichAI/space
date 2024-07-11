from gql import gql


parse_raw_component = gql(
    """
mutation ParseRawComponent($raw_component: String!, $version_mode: String, $org_id: String, $host_id: String, $sync: Boolean) {
  components {
    createFromJson(
      raw: $raw_component
      versionMode: $version_mode
      orgId: $org_id
      hostId: $host_id
      sync: $sync
    ) {
      ... on ComponentUploadType {
        id
        task {
          status
        }
      }
      ... on ComponentType {
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
          flow {
            inFlowComponents {
              edges {
                rel {
                  versionId
                }
                node {
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
                  app {
                    details {
                      uid
                    }
                    op(opType: ["input", "processor", "output"]) {
                      edges {
                        node {
                          details {
                            uid
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
          flow {
            details {
              uid
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
          asset {
            details {
              checksum
              uid
              isComposite
              corePath
            }
            uploadUrl
            downloadUrl
          }
        }
      }
    }
  }
}
""")
