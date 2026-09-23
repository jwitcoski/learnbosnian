import { lazy, Suspense, useState } from "react";
import { Switch, Route, Redirect } from "react-router-dom";
import Footer from "../components/Footer";
import Header from "../components/Header";
import ScrollToTopOnNavigate from "../common/ScrollToTopOnNavigate";
import DocumentTitle from "../common/DocumentTitle";
import { takePrerenderedHtml } from "../common/prerender";
import routes from "./config";
import { Styles } from "../styles/styles";

const PrerenderedFallback = () => {
  const [html] = useState(takePrerenderedHtml);
  return html ? <div dangerouslySetInnerHTML={{ __html: html }} /> : null;
};

const Router = () => {
  return (
    <Suspense fallback={<PrerenderedFallback />}>
      <Styles />
      <ScrollToTopOnNavigate />
      <DocumentTitle />
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
