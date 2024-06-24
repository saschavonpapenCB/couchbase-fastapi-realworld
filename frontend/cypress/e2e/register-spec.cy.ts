/// <reference types="Cypress" />

describe('Register', () => {
  beforeEach(() => {
    cy.task('cleanDatabase')
    cy.visit('/')
    // we are not logged in
  })

  it('registers new user', () => {
    const username = 'visitor'
    const email = 'visitor@email.com'
    const password = 'visiting'
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
