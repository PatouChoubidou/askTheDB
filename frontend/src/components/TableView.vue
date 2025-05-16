—————<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps({ 
  question: String,
  sql: String,
  column_names: Array<string>,
  db_response: String,
  explanation: String
})

// const testString = "[(1, 'John', 'Doe', 'johndoe@example.com', 1), (2, 'Jane', 'SugarBane', 'jane@example.com', 2), (3, 'Peter', 'Parker', 'peter@parker.com', 3), (4, 'Lord', 'The Dark', 'theLord@dark.com', 4), (7, 'Waldon', 'Nesterov', 'wnesterov0@harvard.edu', 41), (8, 'Ramsay', 'Hammerton', 'rhammerton1@dell.com', 40), (9, 'Quentin', 'Boner', 'qboner2@yandex.ru', 37), (10, 'Clayborn', 'Borrow', 'cborrow3@unc.edu', 65), (11, 'Boone', 'Evenden', 'bevenden4@ovh.net', 46), (12, 'Sean', 'Cartmill', 'scartmill5@123-reg.co.uk', 109)]"

const reObjectifyDbResponseString = (str: string)=> {
    // is:  [(1, 'John', 'Doe', 'johndoe@example.com', 1), (2, 'Jane', 'SugarBane',...)]
    // should: [[],[]]
    const tupples = str.match(/(?<=\().+?(?=\))/g) || null;
    console.log('tupples: ',tupples)
    const outputOuterList: string[][] = [];
    if(tupples){
        //loop
        tupples.forEach((tupple) => {
            let outputInnerList: string[] = [];
            const items = tupple.match(/([^\s',]+|'[^']*')+/g)
            console.log('items: ',items);

            if(items){
                items?.forEach((item)=> {
                    item = item.replace(' ', '');
                    item = item.replace('\'', '');
                    item = item.replace('\'', '')
                    outputInnerList.push(item);
                })
            }
            outputOuterList.push(outputInnerList);
        });
        console.log(outputOuterList);
        return outputOuterList
    }     
}


/*
// not nescessary in that case, is sent as array not as string?
const reObjectifyColumnNamesString = (str: string)=> {
    console.log(str)
    // is:  [ 'sting', 'string'] as string
    const arr: string[] = [];
    console.log()

    str = str.replace('[', '');
    str = str.replace(']', '');
    const columns = str.split(',');
    console.log('columns inside reObjectifyColoumnNames', columns)
    columns.forEach((col: string)=>{
        arr.push(col)
    })
    return arr   
}
*/

const list = computed(()=> { return reObjectifyDbResponseString(props.db_response!) || ''})
// const columnList = computed(()=> { return reObjectifyColumnNamesString(props.column_names!) || ''})
 
</script>

<template>
    <div id="table_view_wrapper">
        <table v-if="props.db_response">
           <tr v-if="props.column_names">
                    <th v-for="(columnName) in props.column_names" :key="columnName">{{ columnName }}</th>
            </tr>
            <tr v-for="(items) in list" :key="items[0]">
                <td v-for="item in items " :key="item[0]">{{item}}</td>
            </tr>
        </table>
    </div>
</template>

<style scoped>

#table_view_wrapper{
    font-size: 0.8rem;
    padding: 5px 20px;
    height: 130px;
    width: 100%;
    border-radius: 8px;
    overflow: scroll;
    background-color: var(--color-foreground);
    color: var(--color-background);
}

#table_view_wrapper > table {
    border-collapse: collapse; 
}

#table_view_wrapper > table > tr {
    border-bottom: solid 1px var(--color-background);
}

#table_view_wrapper > table > tr > th {
    font-weight: 800;
    padding: 4px 10px;
}

#table_view_wrapper > table > tr > td {
    padding: 4px 10px;
}

#table_view_wrapper > table > tr > td:first-child {
    font-weight: 800;
}


</style>