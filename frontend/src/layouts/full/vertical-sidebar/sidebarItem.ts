import {
    ApertureIcon,
    LayersLinkedIcon,
    LayoutDashboardIcon, SubtaskIcon, MoodHappyIcon, BrandHipchatIcon, UserPlusIcon
} from 'vue-tabler-icons';

export interface menu {
    header?: string;
    title?: string;
    icon?: any;
    to?: string;
    chip?: string;
    chipColor?: string;
    chipVariant?: string;
    chipIcon?: string;
    children?: menu[];
    disabled?: boolean;
    type?: string;
    subCaption?: string;
}

const sidebarItem: menu[] = [
    { header: 'Home' },
    {
        title: 'Dashboard',
        icon: LayoutDashboardIcon,
        to: '/'
    },
    { header: 'utilities' },
    {
        title: 'Chat',
        icon: BrandHipchatIcon,
        to: '/ui/chat'
    },
    {
        title: 'Graph',
        icon: LayersLinkedIcon,
        to: '/ui/graph'
    },
    // {
    //     title: 'Tasks',
    //     icon: SubtaskIcon,
    //     to: '/ui/tasks'
    // },
    { header: 'auth' },
    {
        title: 'API Keys',
        icon: UserPlusIcon,
        to: '/auth/register'
    },
    { header: 'crawler'},
    {
        title: 'JIRA Wiki',
        icon: '/src/assets/images/icons/jira_wiki.png',
        type: 'image',
        to: '/auth/register'
    },
    {
        title: 'JIRA Task',
        icon: '/src/assets/images/icons/jira_task.png',
        type: 'image',
        to: '/auth/register'
    },
    {
        title: 'Slack Channel',
        icon: '/src/assets/images/icons/slack.png',
        type: 'image',
        to: '/auth/register'
    },
    {
        title: 'Teams Channel',
        icon: '/src/assets/images/icons/teams.png',
        type: 'image',
        to: '/auth/register'
    }
];

export default sidebarItem;
