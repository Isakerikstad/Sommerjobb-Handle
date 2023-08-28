export const streamQuery = `
  query Stream($id: ID!) {
    stream(id: $id) {
      name
      id
      commits {
        totalCount
      }
    }
  }
`
