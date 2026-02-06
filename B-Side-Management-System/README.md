# B-Side Management System (Python & SQLite)

A backend management system designed to centralize organizational data for a multi-branch company, with a focus on clean structure and object-oriented design.

## Project Overview
The system enables managers to manage employees and branches through a command-line interface, while maintaining persistent storage using a relational database.

## Core Functionality
- Management of employees and roles (Worker / Manager)
- Management of company branches (stores)
- Assignment and retrieval of employee and store information
- Persistent data storage using SQLite

## System Design
- Object-Oriented Programming with inheritance (Manager extends Employee)
- Clear separation of concerns:
  - Business logic implemented via domain classes
  - Data persistence handled through a dedicated SQL layer
  - User interaction via a structured CLI loop

## Implementation Notes
- Supports full create, read, and delete flows for employees and stores
- Some update operations are intentionally excluded from the MVP and marked accordingly in the interface

## Tech Stack
Python, SQLite
