// api func

export const createBookmark = async(question: string, sql: string, user_ID: number) => {
    const url = 'http://127.0.0.1:8000/bookmarks/';

    const payload = {
        "question": question || '',
        "sql": sql || '',
        "user_ID": user_ID || 0
    } 

    const request = new Request(url, {
          method: "POST",
          body: JSON.stringify(payload),
    });

    try {
        const response = await fetch(request);
        return response
    } catch (err) {
        console.log(err);
        throw err;
    }
}

export const deleteBookmarkByID = async(id: number) => {
    const url = `http://127.0.0.1:8000/bookmarks/${id}`;

    const request = new Request(url, {
          method: "DELETE",
    });

    try {
        const response = await fetch(request);
        return response
    } catch (err) {
        console.log(err);
        throw err;
    }
}


