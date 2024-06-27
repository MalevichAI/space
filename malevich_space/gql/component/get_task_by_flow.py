from gql import gql

get_task_by_flow = gql(
"""
query GetComponentByReverseID($uid: String!, $status:[String!]) {
  tasks {
    flow(uid: $uid, bootState: $status, first: 10000000) {
      edges {
        node {
          details {
            uid
            lastRunnedAt
          }
        }
      }
    }
  }
}
"""
)
