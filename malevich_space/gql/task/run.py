from gql import gql


run_task = gql(
    """
    mutation RunCoreTask($task_id: String!, $raw: String, $org_id: String, $ca_override: [CAOverride!], $webhook: [String!]) {
      runWithStatus(
        taskId: $task_id,
        orgId: $org_id
        input: {
          node: {
              webhook: $webhook
          }
          raw: $raw
          caOverride: $ca_override
        }
      ) {
        details {
          uid
        }
      }
    }
    """
)
