from gql import gql


create_branch = gql(
    """
    mutation CreateBranch($component_id: String!, $name: String!, $status: String!, $comp_rel_status: String!) {
      component(uid: $component_id) {
        createBranch(
          input: {
            node: {
              name: $name,
              status: $status
            },
            rel: {
              status: $comp_rel_status
            }
          }
        ) {
          details {
            uid
            name
          }
        }
      }
    }
    """
)
