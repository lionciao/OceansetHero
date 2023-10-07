<script setup lang="ts">

import { ref, toRefs } from 'vue';
import axios from 'axios';

const searchQuery = ref('');
const searchResults = ref([]);
const showList = ref(false);

const props = defineProps<{
    handleListItemClick: Function
}>()

const clearSearch = () => {
    searchQuery.value = '';
    searchResults.value = [];
};

const handleSearch = async () => {
    const apiUrl = `https://www.oceanset.earth/api/search?q=${searchQuery.value}`;

    if (searchQuery.value.length > 0) {
        axios.get(apiUrl)
            .then((response) => {
                searchResults.value = response.data;
                showList.value = true;
            })
            .catch((error) => {
                console.error(error);
            });
    } else {
        searchResults.value = [];
        showList.value = false;
    }
};



</script>

<template>
    <div class="search-container">
        <div class="search-bar">
            <input type="text" v-model="searchQuery" placeholder="Search..." @input="handleSearch" />
            <button @click="clearSearch">
                <img src="@/views/earth/search-30.svg">
            </button>
        </div>
        <ul class="search-results" v-show="showList && searchResults.length > 0">
            <li class="rec-word">Recommended Search Locations</li>
            <li v-for="(result, index) in searchResults" :key="result.id" @click="() => {showList=false; props.handleListItemClick(result);}"
                style=" display: flex;">
                <img src="@/views/earth/location.svg" style="width: 30px;">
                <div style="margin-left: 10px;">
                    <div style="font-size: 18px;">{{ result.name }}</div>
                    <div style="font-size: 12px; color: #7C7C80;">{{ result.region }}</div>
                </div>
            </li>
        </ul>
    </div>
</template>

<style>
.search-container {
    position: relative;
    width: 100%;
    /* background-color: #000000; */
}

.search-bar {
    display: flex;
    /* align-items: center; */
    border: 1px solid #ccc;
    border-radius: 4px;
    padding: 5px;
    background-color: #fdfcfcba;
    color: #000000;
}

input[type="text"] {
    flex-grow: 1;
    border: none;
    outline: none;
    padding: 5px;
    color: #000000;
}

button {
    border: none;
    background: none;
    cursor: pointer;
    padding: 5px;
}

.fa-search {
    font-size: 18px;
}

.search-results {
    width: 974px;
    position: absolute;
    top: 100%;
    left: 0;
    list-style: none;
    margin-top: 10px;
    background-color: #fdfcfcba;
    border: 1px solid #ccc;
    z-index: 999;
}

.search-results li {
    width: 100%;
    padding: 10px;
    border-top: 1px solid #ccc;
}

.rec-word {
    height: 17px;
    font-size: 12px;
    font-weight: bolder;
    color: #7C7C80;
}
</style>
