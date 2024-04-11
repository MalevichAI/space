from gql import gql


auto_layout = gql("""
    query AutoLayout($flow: String!) {
        flow(uid: $flow) {
            autoLayout {
                pageInfo {
                    totalLen
                }
            }
        }
    }
    """)