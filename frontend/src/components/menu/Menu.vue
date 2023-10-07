<template>
    <v-container
        style="color:white; padding-top:57px; background-image: url('src/assets/images/svg.svg'); background-size: cover; background-repeat: no-repeat; background-position: center center;">
        <v-row>
            <v-col style="font-size:14px">
                <b>Access Water Quality Information for a Location</b>
            </v-col>
        </v-row>

        <v-row>
            <v-col style="font-size:20px">
                <v-icon color="white" icon="mdi-map-marker"></v-icon>
                <b>{{ habitatName }}</b>
            </v-col>
        </v-row>

        <v-row>
            <v-col style="padding: 12px 6px 12px 6px;" cols="4" v-for="(quality, index) in qualities" :key="index">
                <!-- <img style="width: 28%; position:absolute" src="@/assets/images/rec.png" /> -->
                <div
                    style="padding-top:12px ;width: 109px; height: 74px; flex-shrink: 0; text-align: center; border-radius: 12px; background: rgba(255, 255, 255, 0.24); box-shadow: 0px 4px 40px 0px rgba(255, 255, 255, 0.12); backdrop-filter: blur(16px);">
                    <div
                        style="color: #FFF; text-align: center; font-feature-settings: 'clig' off, 'liga' off; font-size: 12px; font-style: normal; font-weight: 400; line-height: 20px;  letter-spacing: -0.24px;">
                        {{ quality.name }}</div>
                    <div
                        style="color: #FFF; text-align: center; font-feature-settings: 'clig' off, 'liga' off; font-size: 20px; font-style: normal; font-weight: 600; line-height: 20px;  letter-spacing: -0.24px;">
                        {{ quality.value ? `${quality.value} µg/L` : '--' }}</div>
                </div>
            </v-col>
        </v-row>

        <v-row style="margin-bottom: 10px;">
            <v-col style="font-size: 12px; font-weight: 500;line-height: 20px; letter-spacing: -0.12px;">
                <b>Last updated time: {{ getYesterday() }} <br />Updated every 24 hours.</b>
            </v-col>
        </v-row>

        <v-row align="center" style="background-color: #1E6AFF; padding: 0; margin: -15px;">
            <v-col cols="1" style="font-size: 20px;">✨</v-col>
            <v-col cols="8"
                style="color: #FFF;font-size: 12px;font-style: normal;font-weight: 400;line-height: 14px; letter-spacing: -0.24px;"><b>How
                    does the water source in this area come about?</b></v-col>
            <v-col cols="3">
                <v-dialog transition="dialog-bottom-transition" width="900px" height="657px">
                    <template v-slot:activator="{ props }">
                        <v-btn color="rgba(30,106,255,1)" flat size="small"
                            style="display: flex; justify-content: center; align-items: center; gap: 10px;border-radius: 100px; border: 1px solid #FFF;"
                            v-bind="props"><b>Check</b></v-btn>
                    </template>
                    <template v-slot:default="{ isActive }">
                        <v-card>
                            <v-toolbar color="white" title="How does the water source in this area come about"></v-toolbar>
                            <v-divider></v-divider>
                            <v-card-text>
                                <iframe width="850" height="450" :src="windyURL" frameborder="0"></iframe>

                                <p
                                    style="color: var(--color-gray-080, #7C7C80); font-size: 14px; font-style: normal; font-weight: 400; line-height: 20px; letter-spacing: -0.14px;">
                                    Resources: {{ windyURL }}</p>
                            </v-card-text>
                        </v-card>
                    </template>
                </v-dialog>
            </v-col>
        </v-row>
    </v-container>
    <v-tabs fixed-tabs color="#3473F0" style="color:#7C7C80" v-model="tab">
        <v-tab>✨ AI analysis</v-tab>
        <v-tab>Endangered <br />Species</v-tab>
        <v-tab>Activity <br /> Suggestions</v-tab>
    </v-tabs>
    <v-window v-model="tab">
        <v-window-item style="padding:10px;">
            <v-container>
                <v-row style="color: #141A1E; font-size: 20px;">
                    <v-col style="padding-bottom:5px; display: flex;">
                        <b>✨ AI analysis</b> &nbsp;&nbsp;&nbsp; <img src="@/assets/images/azure-ai.svg" />
                    </v-col>
                </v-row>
                <v-row style="font-size:14px; color: #7C7C80; margin-top: 10px">
                    <v-col>
                        Utilize DataStream for water monitoring data and apply OpenAI analysis to empower users with
                        simplified, accessible insights into water quality.
                    </v-col>
                </v-row>
                <v-row style="border-radius: 12px; background: #F6F6F9; margin-top: 15px; min-height: 45vh;">
                    <p style="padding:12px;">
                        {{ analyzeContent }}
                    </p>
                    <v-progress-circular style="position: absolute; right: 12vw; top: 28vh" v-if="analyzeContent == ''"
                        :size="80" color="primary" indeterminate></v-progress-circular>
                </v-row>
            </v-container>
        </v-window-item>
        <v-window-item style="padding:10px;">
            <v-container>
                <v-row style="font-size:20px; color: #141A1E;">
                    <v-col style="padding-bottom:5px">
                        <b>Aquatic species at risk</b>
                    </v-col>
                </v-row>
                <v-row style="font-size:14px; color: #7C7C80; margin-top: 10px">
                    <v-col>
                        In understanding which endangered animals inhabit the area and how to protect them
                    </v-col>
                </v-row>
            </v-container>
            <v-container style=" padding: 0px; margin: 0" v-for="(species, index) in species" :key="index">
                <a :href="species.link" target="_blank">
                    <v-icon style="position:absolute; right:23px; top:130px; z-index:2" color="#4B82EF"
                        icon="mdi-open-in-new"></v-icon>
                </a>
                <v-container style="z-index:2; width: 100%; border: 1px solid #D0DBE2; border-radius: 8px;">
                    <v-row align="center">
                        <v-col cols="2">
                            <img style="width: 48px; height:48px; object-fit: cover; border-radius: 8px"
                                :src="species.url" />
                        </v-col>
                        <v-col>
                            <div style="color:#7C7C80; font-size:12px">{{ species.toxo }}</div>
                            <div style="color:#2C2C32; font-size:14px"><b>{{ species.name }}</b></div>
                        </v-col>
                    </v-row>
                    <v-row>
                        <v-col style="padding-top: 5px">
                            <div style="color:#7C7C80; font-size:10px">{{ species.description }}</div>
                        </v-col>
                    </v-row>
                </v-container>
            </v-container>
        </v-window-item>
        <v-window-item style="padding:10px;">
            <v-container>
                <v-row style="font-size:20px; color: #141A1E;">
                    <v-col style="padding-bottom:5px">
                        <b>What Activity Are You Planning</b>
                    </v-col>
                </v-row>
                <v-row style="font-size:14px; color: #7C7C80;  margin-top: 10px">
                    <v-col>
                        Recommendations Based on Activity Type
                    </v-col>
                </v-row>
            </v-container>
            <v-container style=" padding: 0px; margin: 0" v-for="(action, index) in actions" :key="index">
                <v-container style="z-index:2; width: 100%; border: 1px solid #D0DBE2; border-radius: 8px;">
                    <v-row align="center">
                        <v-col cols="1">
                            {{ action.icon }}
                        </v-col>
                        <v-col>
                            <div
                                style="color: var(--neutral-1, #141A1E); font-size: 14px; font-style: normal; font-weight: 600; line-height: 24px; letter-spacing: -0.14px;">
                                <b>{{ action.name }}</b>
                            </div>
                            <div
                                style="color: var(--color-gray-080, #7C7C80); font-size: 12px; font-style: normal; font-weight: 400; line-height: 14px;">
                                {{ action.comment }}</div>
                        </v-col>
                    </v-row>
                    <v-row>
                        <v-col style="padding-top: 5px">
                            <div
                                style="color: #000;font-size: 12px; font-style: normal; font-weight: 400; line-height: 18px; /* 150% */ letter-spacing: -0.12px;">
                                {{ action.description }}</div>
                        </v-col>
                    </v-row>

                    <v-row>
                        <v-col style="padding-bottom: 0px;">
                            <img v-if="action.status == 'NOT_RECOMMENDED'" src="@/assets/images/not-recommended.svg" />
                            <img v-if="action.status == 'PERFORM_WELL'" src="@/assets/images/perform-well.svg" />
                        </v-col>
                    </v-row>
                </v-container>
                <br />
            </v-container>
        </v-window-item>
    </v-window>
</template>

<script setup lang="ts">
import { watch } from 'vue'
import { ref, onMounted } from 'vue'
import axios from 'axios'

const props = defineProps<{
    habitatID: number
}>()

const actionMap = {
    'swimming': {
        'name': 'Swimming',
        'icon': '🏊‍♀️',
        'comment': 'Against waterborne illnesses during activities.',
        'statusMap': {
            'NOT_RECOMMENDED': 'This area is not recommended for swimming due to the presence of endangered species. Engaging in activities in this area might harm the local ecosystem. We recommend visiting the page related to this endangered species for more information to ensure their protection.',
            'PERFORM_WELL': 'This area is safe for swimming, and the water here meets drinking standards. You can enjoy the water here with peace of mind.'
        }
    },
    'eating': {
        'name': 'Eating Fish',
        'icon': '🐟',
        'comment': 'Assessing the consumption levels of fish and shellfish, and also water pollution.',
        'statusMap': {
            'NOT_RECOMMENDED': 'This area is not recommended for eating fish due to the presence of endangered species. Engaging in activities in this area might harm the local ecosystem. We recommend visiting the page related to this endangered species for more information to ensure their protection.',
            'PERFORM_WELL': "This area doesn't have endangered species, and the water is safe to drink. You can safely eat fish here.",
        }
    },
    'drinking': {
        'name': 'Drinking Water',
        'icon': '💧',
        'comment': 'Assessing whether the water in the area is suitable for direct consumption.',
        'statusMap': {
            'NOT_RECOMMENDED': "The chemical composition of the water in this area doesn't meet drinking standards. Without proper treatment, it's not safe to drink directly. We recommend not drinking the water from this area without treatment.",
            'PERFORM_WELL': `The chemical composition of the water in this area doesn't meet drinking standards. Without proper treatment, it's not safe to drink directly. We recommend not drinking the water from this area without treatment.`,
        }

    }
}

const defaultQualities = [
    {
        'name': 'arsenic',
        'value': null,
        'status': 'PASS'
    },
    {
        'name': 'copper',
        'value': null,
        'status': 'PASS'
    },
    {
        'name': 'lead',
        'value': null,
        'status': 'PASS'
    }
]

const species = ref([])
const habitatName = ref("")
const actions = ref([])
const qualities = ref(defaultQualities)
const tab = ref(0)
const windyURL = ref("https://embed.windy.com/embed2.html?lat=10.922&lon=-169.031&detailLat=10.922&detailLon=-169.031&width=650&height=450&zoom=6&level=surface&overlay=currents&product=cmems&menu=&message=&marker=&calendar=now&pressure=&type=map&location=coordinates&detail=&metricWind=default&metricTemp=default&radarRange=-1")
const analyzeContent = ref("")

const _sleep = (ms: number) => {
    return new Promise(resolve => setTimeout(resolve, ms));
}

const getYesterday = () => {
  const today = new Date();
  const yesterday = new Date(today);
  yesterday.setDate(today.getDate() - 1);
  const year = yesterday.getFullYear();
  const month = (yesterday.getMonth() + 1 < 10 ? '0' : '') + (yesterday.getMonth() + 1);
  const day = (yesterday.getDate() < 10 ? '0' : '') + yesterday.getDate();

  return `${year}/${month}/${day} 00:23`;
}

const buildActions = (sourceActions) => {
    const result = [];

    for (const sourceAction of sourceActions) {
        const key = sourceAction.name;
        const source = actionMap[key];
        const action = {
            'name': source.name,
            'icon': source.icon,
            'comment': source.comment,
            'description': source.statusMap[sourceAction.status],
            'status': sourceAction.status
        }
        result.push(action)
    }

    return result
}

const setHabitat = async (habitatID) => {
    axios.get(`https://www.oceanset.earth/api/describe/${habitatID}`)
        .then((res) => {
            const data = res.data
            console.log('describe data', data)
            species.value = data.species
            habitatName.value = data.name
            actions.value = buildActions(data.actions)
            qualities.value = data.quality

            const [lon, lat] = data.centre
            windyURL.value = `https://embed.windy.com/embed2.html?lat=${lat}&lon=${lon}&detailLat=${lat}&detailLon=${lon}&width=650&height=450&zoom=6&level=surface&overlay=currents&product=cmems&menu=&message=&marker=&calendar=now&pressure=&type=map&location=coordinates&detail=&metricWind=default&metricTemp=default&radarRange=-1`
        }).catch((err) => {
            console.log('err', err)
        })

    analyzeContent.value = ""
    axios.get(`https://www.oceanset.earth/api/analyze/${habitatID}`).then(async (res) => {
        const data = res.data
        analyzeContent.value = ""

        for (let word of data.content.split(' ')) {
            analyzeContent.value += word + ' '
            await _sleep(Math.random() * 100)
        }
    }).catch((err) => {
        console.log('err', err)
    })
}

watch(() => props.habitatID, async (habitatID) => {
    console.log('habitatID', habitatID)
    if (habitatID) {
        await setHabitat(habitatID)
    }
})

onMounted(async () => {
    await setHabitat(props.habitatID)
})

</script>

<style>
.v-slide-group-item--active {
    color: #3473F0
}
</style>