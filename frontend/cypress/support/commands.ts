/// <reference types="cypress" />

const apiUrl = Cypress.env('apiUrl')

declare global {
    namespace Cypress {
      interface Chainable<Subject = any> {
        registerUserIfNeeded(options?: Partial<{ email: string; password: string; username: string; image: string }>): Chainable<void>;
        getLoginToken(user?: { email: string; password: string }): Chainable<string>;
        login(user?: { email: string; password: string }): Chainable<void>;
      }
    }
  }

  // creates a user with email and password
  // defined in cypress environment variables
  // if the user already exists, ignores the error
  // or given user info parameters
  Cypress.Commands.add('registerUserIfNeeded', (options = {}) => {
    const defaults = {
      image: 'https://robohash.org/couchbasecapella?set=set3&size=150x150',
      // email, password
      ...Cypress.env('user')
    };
    const user = Cypress._.defaults({}, options, defaults);
    cy.request({
      method: 'POST',
      url: `${apiUrl}/api/users`,
      body: {
        user,
      },
      failOnStatusCode: false
    });
  });



  // custom Cypress command to simply return a token after logging in
  // useful to perform authorized API calls
  Cypress.Commands.add('getLoginToken', (user = Cypress.env('user')) => {
    return cy
      .request('POST', `${Cypress.env('apiUrl')}/api/users/login`, {
        user: Cypress._.pick(user, ['email', 'password'])
      })
      .its('body.user.token')
      .should('exist')
      .then((token: string) => {
        return token; // Return the token obtained
      });
  });

  Cypress.Commands.add('login', (user = Cypress.env('user')) => {
    cy.getLoginToken(user).then(token => {
      localStorage.setItem('jwt', token);
      // with this token set, when we visit the page
      // the web application will have the user logged in
    });
  });
  
  export {};