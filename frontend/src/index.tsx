import { BrowserRouter } from "react-router-dom";
import ReactDOM from "react-dom";
import { I18nextProvider } from "react-i18next";
import 'antd/dist/antd.min.css';

import Router from "./router";
import i18n from "./translation";
import { capturePrerenderedHtml } from "./common/prerender";

const App = () => (
  <BrowserRouter>
    <I18nextProvider i18n={i18n}>
      <Router />
    </I18nextProvider>
  </BrowserRouter>
);

const rootElement = document.getElementById("root") as HTMLElement;
capturePrerenderedHtml(rootElement);

ReactDOM.render(<App />, rootElement);
