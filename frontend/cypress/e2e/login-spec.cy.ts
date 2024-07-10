/// <reference types="cypress" />

describe('Conduit Login', () => {
  before(() => {
    cy.registerUserIfNeeded();
  });

  beforeEach(() => {
    cy.visit('/');
    // we are not logged in
  });

  it('does not work with wrong credentials', () => {
    cy.contains('li', 'Sign in').click();

    cy.get('input[type="email"]').type('wrong@email.com');
    cy.get('input[type="password"]').type('no-such-user');
    cy.get('button[type="submit"]').click();

    // We remain on the login page
    cy.url().should('contain', '/login');
  });

  it('logs in', () => {
    cy.contains('li', 'Sign in').click();
  
    const user = Cypress.env('user') as { email: string; password: string }; // Type assertion for user object
    cy.get('input[type="email"]').type(user.email);
    cy.get('input[type="password"]').type(user.password);
    cy.get('button[type="submit"]').click();
  
    // when we are logged in, there should be two feeds
    cy.contains('span.nav-link', 'Your Feed').should('have.class', 'active');
    cy.contains('span.nav-link', 'Global Feed').should('not.have.class', 'active');
    // url is /
    cy.url().should('not.contain', '/login');
  });
  

});