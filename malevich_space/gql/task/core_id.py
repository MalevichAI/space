from gql import gql


get_task_core_id = gql("""
    query GetTaskCoreId($task_id: String!) {
        task(uid: $task_id) {
            details {
                coreId
            }
            component {
                details {
                    reverseId
                }
            }
        }
    }
    """)
