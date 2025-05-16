
export const apiSendQ = async(q: string) => {

  const url = 'http://127.0.0.1:8000/askLLM/' ;
  const payload = {
    "question": q || '',
  } 
  const request = new Request(url, {
      method: "POST",
      body: JSON.stringify(payload),
  });
  const response = await fetch(request);
  return response 
}


export const apiSendSQL = async(question: string, sql: string) => {
    // sanitize question of line breaks
    question = question.replace(/(\r\n|\n|\r)/gm, "");

    const url = 'http://127.0.0.1:8000/sendSQL/' ;
    const payload2 = {
      "sql": sql,
      "question": question 
    } 
    const request = new Request(url, {
        method: "POST",
        body: JSON.stringify(payload2),
    });
    
    const response = await fetch(request);
    return response   
} 


 