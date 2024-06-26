import { createRouter, createWebHistory } from 'vue-router';
import DashboardScreen from '@/components/DashboardScreen.vue';
import RoadmapScreen from '@/components/RoadmapScreen.vue';
import EditionScreen from '@/components/EditionScreen.vue';

const routes = [
  { path: '/dashboard', component: DashboardScreen },
  { path: '/roadmap', component: RoadmapScreen },
  { path: '/edition', component: EditionScreen },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
