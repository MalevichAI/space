from gql import gql

get_version_by_task_id = gql(
    """
    query GetBranchByName($task_id: String!) {
        task(uid: $task_id) {
            version {
                details {
                    uid
                }
            }
        }
    }
    """
)

get_branch_by_task_id = gql(
    """
    query GetBranchByName($task_id: String!) {
        task(uid: $task_id) {
            branch {
                details {
                    uid
                    name
                    status
                }
            }
        }
    }
    """
)