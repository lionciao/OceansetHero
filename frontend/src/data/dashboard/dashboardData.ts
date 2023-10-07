import type { recentTrans, productPerformanceType, productsCards } from '@/types/dashboard/index';

/*--Recent Transaction--*/
const recentTransaction: recentTrans[] = [
    {
        title: '09:32 am',
        subtitle: 'Crawl from JIRA wiki',
        textcolor: 'primary',
        boldtext: false,
        line: true,
        link: '',
        url: ''
    },
    {
        title: '10:17 am',
        subtitle: 'Crawl from JIRA tasks',
        textcolor: 'secondary',
        boldtext: false,
        line: true,
        link: '#C1FSS, #V1Pair',
        url: ''
    },
    {
        title: '12:23 am',
        subtitle: 'Crawl from Teams',
        textcolor: 'success',
        boldtext: false,
        line: true,
        link: '',
        url: ''
    },
    {
        title: '2:30 pm',
        subtitle: 'Crawl from slack channel',
        textcolor: 'success',
        boldtext: true,
        line: true,
        link: '#general, #random, #project-updates',
        url: ''
    }
]

/*Basic Table 1*/
const productPerformance: productPerformanceType[] = [
    {
        id: 1,
        name: 'JIRA tasks',
        post: '',
        pname: '00:36:21',
        status: 'Finish',
        statuscolor: 'primary',
        budget: '63'
    },
    {
        id: 2,
        name: 'Public Slack Channel',
        post: '',
        pname: '01:12:03',
        status: 'Finish',
        statuscolor: 'primary',
        budget: '42'
    },
    {
        id: 3,
        name: 'JIRA wiki',
        post: '',
        pname: '12:31',
        status: 'Crawling',
        statuscolor: 'secondary',
        budget: '-'
    },
    {
        id: 4,
        name: 'Public Teams Channel',
        post: '',
        pname: '-',
        status: 'Waiting',
        statuscolor: 'success',
        budget: '-'
    }
];

/*--Products Cards--*/
import proimg1 from '@/assets/images/products/s4.jpg';
import proimg2 from '@/assets/images/products/s5.jpg';
import proimg3 from '@/assets/images/products/s7.jpg';
import proimg4 from '@/assets/images/products/s11.jpg';
const productsCard: productsCards[] = [
    {
        title: 'Boat Headphone',
        link: '/',
        photo: proimg1,
        salesPrice: 375,
        price: 285,
        rating: 4
    },
    {
        title: 'MacBook Air Pro',
        link: '/',
        photo: proimg2,
        salesPrice: 650,
        price: 900,
        rating: 5
    },
    {
        title: 'Red Valvet Dress',
        link: '/',
        photo: proimg3,
        salesPrice: 150,
        price: 200,
        rating: 3
    },
    {
        title: 'Cute Soft Teddybear',
        link: '/',
        photo: proimg4,
        salesPrice: 285,
        price: 345,
        rating: 2
    }
];


export { recentTransaction, productPerformance, productsCard }