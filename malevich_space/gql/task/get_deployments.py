from gql import gql


get_deployments_for_reverse_id = gql(
    """
    query GetDeploymentsForReverseId($reverse_id: String!, $status: [String!]) {
        tasks {
            component(componentId: [$reverse_id], status: $status) {
                edges {
                    node {
                        details {
                            uid
                            coreId
                            bootState
                            lastRunnedAt
                        }
                    }
                }
            }
        }
    }
    """
)
