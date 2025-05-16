
export const apiSendRating = async(question: string, sql: string, db_response:string, explanation:string, user_ID: number, q_interpretation: number, sql_quality: number ) => {
    const url = 'http://127.0.0.1:8000/ratings/' ;
    const payload = {
        "question": question,
        "sql": sql,
        "db_response": db_response,
        "explanation": explanation,
        "user_ID": user_ID,
        "q_interpretation": q_interpretation,
        "sql_quality": sql_quality 
    } 
    const request = new Request(url, {
        method: "POST",
        body: JSON.stringify(payload),
    });
    const response = await fetch(request);
    return response     
}