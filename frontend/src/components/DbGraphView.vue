—————<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { toRaw } from 'vue';
import { useTableStore } from '../stores/db_tables.ts'
import type { createStmtNode, createStmtEdge } from '../interfaces'
// @ts-ignore
import cytoscape from '../assets/scripts/cytoscape.esm.mjs' 


const { getNodesArray } = useTableStore()
const createStmtNodeList = ref([] as createStmtNode[]);

onMounted(async() => {
    createStmtNodeList.value = await getNodesArray() || [];
    console.log("nodes array from view : ",  toRaw(createStmtNodeList.value)); 
    const myEles = await cyConformNodeList();
    await myCy(myEles);  
})

const cyConformNodeList = async() => {
    let myNodes = [];
    let myEdges = [];
    for(let i = 0; i < createStmtNodeList.value.length; i++){
        //console.log(toRaw(createStmtNodeList.value[i]))
        const newNode = {"data": {"id": toRaw(createStmtNodeList.value[i])["name"].toLocaleLowerCase()}}
        myNodes.push(newNode)
        const nodesEdges: createStmtEdge[] = toRaw(createStmtNodeList.value[i])["edges"];
        // console.log(nodesEdges)
        if(nodesEdges.length){
            for(let i=0; i < nodesEdges.length; i++){
                console.log(nodesEdges[i])
                const edge = nodesEdges[i]
                const id = (edge.start + '_'+  edge.end).toLocaleLowerCase().replace(' ', '');
                const start = edge.start.toLocaleLowerCase().replace(' ', '');
                const end = edge.end.toLocaleLowerCase().replace(' ', '');
                const newEdge = {"data": {
                    "id": id,
                    "source": start,
                    "target": end
                    }
                }
                myEdges.push(newEdge)
            }
        }
    }
    
    const myElements = myNodes.concat(myEdges);
    return myElements
}

const myCy = async(myEles: { data: { id: string; }; }[] | { data: { id: string, source: string, target: string }; }[] | [])=> {
    console.log('inside cy', myEles);
    
    const cy = cytoscape({
        container: document.getElementById('cy'), // container to render in
       
        elements: myEles,

        style: [ // the stylesheet for the graph
        {
            selector: 'node',
            style: {
            'background-color': '#f0f0f0',
            'background-opacity': '0',
            'border-width': '4px',
            'border-color': '#0099e6',
            'label': 'data(id)',
            }
        },

        {
            selector: 'edge',
            style: {
            'width': 2,
            'line-color': '#ccc',
            'target-arrow-color': '#ccc',
            'target-arrow-shape': 'triangle',
            'curve-style': 'bezier'
            }
        },
        {
            selector: 'label',
            style: {
            'text-background-opacity': '0',
            'text-background-padding': '0',
             'text-background-color': '#f0f0f0',
             'text-margin-y': '-5px',
             'font-size': '0.8em',
             'color': '#0099e6'
            }
        },
        ],

        layout: {
        name: 'cose',
        }
    });
   
    var layout = cy.layout({ name: 'cose' });
    layout.run();
    // some time later...
    setTimeout(function(){
        layout.stop();
    }, 100);   
}



</script>

<template>
    <div id="db_graph_wrapper">
        
        <div id="cy"></div>  
        <div>database map</div>
    </div>
</template>

<style scoped>

#db_graph_wrapper {
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
    position: absolute;
    top: 0;
    left: 0;
    z-index: 1;
    background-color:none;
    display: none;
}

#cy {
    width: 30vw;
    height: 80vh;
}

@media (min-width: 1024px) {
    #db_graph_wrapper {
        display: flex;
    }

    
}

</style>