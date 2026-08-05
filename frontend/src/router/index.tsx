import { lazy, Suspense } from "react";
import { Switch, Route, Redirect } from "react-router-dom";
import Footer from "../components/Footer";
import Header from "../components/Header";
import ScrollToTopOnNavigate from "../common/ScrollToTopOnNavigate";
import routes from "./config";
import { Styles } from "../styles/styles";

const Router = () => {
  return (
    <Suspense fallback={null}>
      <Styles />
      <ScrollToTopOnNavigate />
      <Header />
      <Switch>
        <Route
          path="/learn/day/:n"
          exact
          render={({ match }) => (
            <Redirect to={`/learn/lesson/${match.params.n}`} />
          )}
        />
        <Route
          path="/quiz/day/:n"
          exact
          render={({ match }) => (
            <Redirect to={`/quiz/lesson/${match.params.n}`} />
          )}
        />
        {routes.map((routeItem) => {
          return (
            <Route
              key={routeItem.component}
              path={routeItem.path}
              exact={routeItem.exact}
              component={lazy(() => import(`../pages/${routeItem.component}`))}
            />
          );
        })}
      </Switch>
      <Footer />
    </Suspense>
  );
};

export default Router;
