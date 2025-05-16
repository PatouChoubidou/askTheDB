import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import type { createStmtNode, createStmtEdge } from '../interfaces'


export const useTableStore = defineStore('table', () => {

    interface Statement {
        stmt: string;
    } 

    const tables = ref([] as string[]);
    const createTableArray = ref([] as Array<Statement>)
    const nodesArray = ref([] as Array<createStmtNode>)
    const error = ref('')

    const fetchTables = async() => {
        const url = 'http://127.0.0.1:8000/getTables/';
        try {
            const response = await fetch(url);
            const json = await response.json();
            console.log(json);
            tables.value = json['tables']; 
        } catch (err) {
            console.log(err);
            error.value = 'the error was' + err
        }
    }

    const fetchCreateTableArray = async() => {
        const url = 'http://127.0.0.1:8000/getCreateStmts/';
        try {
            const response = await fetch(url);
            const json = await response.json();
            console.log(json);
            createTableArray.value = json; 
        } catch (err) {
            console.log(err);
            error.value = 'the error was' + err
        }
    }

    const getNodesArray = async() => {
        await fetchCreateTableArray();
        const nodeArr = [] as createStmtNode[];
        if(createTableArray.value){
            for(let i = 0; i < createTableArray.value.length; i++) {
                const newNode = await deconstructCreateStmt(createTableArray.value[i]['stmt']) || null;
                if(newNode) { nodeArr.push(newNode) }
            }
        } 
        return nodeArr
    }

    const deconstructCreateStmt = async(stmt: string) => {
        /*
         "stmt": "CREATE TABLE OrderDetails (\n        order_detail_ID INTEGER PRIMARY KEY AUTOINCREMENT,\n        order_ID INTEGER NOT NULL,\n        product_ID INTEGER NOT NULL,\n        quantity INTEGER NOT NULL,\n        subtotal REAL NOT NULL,\n        FOREIGN KEY (order_ID) REFERENCES Orders(order_ID),\n        FOREIGN KEY (product_ID) REFERENCES Products(product_ID)\n )"
        */
        let output = null;
        let currentTableName = "";
        
        // get the table name / node
        const regex1 = /(?<=CREATE TABLE ).*?(?= \()/gm;
        const tableNames = stmt.match(regex1);
        
        if(tableNames){
            currentTableName = tableNames[0]  
        }
    
        // get the table relations / egdes
        const edgeArr = [] as createStmtEdge[];
        const regex2 = /(?<=REFERENCES ).*?(?=\()/gm;
        const relations = stmt.match(regex2);
        if(relations){
            for (let i=0; i < relations.length; i++) {
                const newEdge: createStmtEdge = {
                    start: currentTableName,
                    end: relations[i]
                }
                edgeArr.push(newEdge)      
            }  
         
        }
        const newNode: createStmtNode = {
            name: currentTableName,
            edges: edgeArr
        }
        output = newNode
        // console.log("newNode: ", newNode)
        return output
    }

    return { tables, fetchTables, createTableArray, fetchCreateTableArray, nodesArray, getNodesArray, error}
})

