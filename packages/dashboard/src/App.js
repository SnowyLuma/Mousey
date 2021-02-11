import React, { lazy, Suspense } from "react";
import { BrowserRouter, Switch, Route } from "react-router-dom";

import "./App.css";
import "./colors.css";

const Archive = lazy(() => import("./Archive"));

function Loading() {
  return <div className="status">Loading website ...</div>;
}

function NotFound() {
  return <div className="status error">There's nothing to be found here! :(</div>;
}

export default function App() {
  return (
    <BrowserRouter>
      <Suspense fallback={<Loading />}>
        <Switch>
          <Route path="/archives/:id">
            <Archive />
          </Route>
          <Route path="*">
            <NotFound />
          </Route>
        </Switch>
      </Suspense>
    </BrowserRouter>
  );
}