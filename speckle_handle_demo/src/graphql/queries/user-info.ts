// @/graphql/queries/user-info.ts
export const userInfoQuery = `query {
    activeUser {
      email
      name
      company
      bio
      avatar
    }
  }`
