
export interface Bookmark {
    bookmark_ID: number
    question: string,
    sql: string,
    user_ID: number,
    created_at: string
}

export interface User {
    user_ID: number,
    username: string,
    email: string,
    disabled: number,
    created_at: string
}

export interface createStmtEdge {
    start: string,
    end: string
}

export interface createStmtNode {
    name: string,
    edges: createStmtEdge[]
}




