import { createRouter, createWebHistory } from 'vue-router';
import DashboardScreen from '@/components/DashboardScreen.vue';
import RoadmapScreen from '@/components/RoadmapScreen.vue';

const routes = [
  { path: '/dashboard', component: DashboardScreen },
  { path: '/roadmap', component: RoadmapScreen },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
