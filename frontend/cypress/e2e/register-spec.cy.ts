/// <reference types="Cypress" />

describe('Register', () => {
  beforeEach(() => {
    cy.visit('/')
    // we are not logged in
  })

  it('registers new user', () => {
    const username = 'tester'
    const email = 'tester@test.com'
    const password = 'password1234'
    cy.contains('li', 'Sign up').click();

    cy.url().should('include', '/register')
    cy.get('input[formcontrolname="username"]').type(username)
    cy.get('input[formcontrolname="email"]').type(email)
    cy.get('input[formcontrolname="password"]').type(password)
    cy.get('form').submit()

    cy.location('pathname').should('equal', '/')
    cy.contains(username).should('be.visible')
  })
})
