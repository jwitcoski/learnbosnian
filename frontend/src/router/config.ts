const routes = [
  {
    path: ["/", "/home"],
    exact: true,
    component: "Home",
  },
  {
    path: "/learn",
    exact: true,
    component: "Learn",
  },
  {
    path: "/learn/lesson/:n",
    exact: true,
    component: "Day",
  },
  {
    path: "/quiz/lesson/:n",
    exact: true,
    component: "Quiz",
  },
  {
    path: "/dictionary",
    exact: true,
    component: "Dictionary",
  },
  {
    path: "/books",
    exact: true,
    component: "Books",
  },
  {
    path: "/attributions",
    exact: true,
    component: "Attributions",
  },
];

export default routes;
