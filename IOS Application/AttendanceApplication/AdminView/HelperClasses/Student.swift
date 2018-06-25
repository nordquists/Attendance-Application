//
//  Student.swift
//  AttendanceApplication
//

import Foundation
import UIKit
import Alamofire

class Student {
    
    // MARK: Public Properties
    
    var name: String!
    var email: String!
    var id: String!
    var recentLocations: [Location] = []
    
    // MARK: Init
    
    init(studentJSONObject: [String: String]) {
        /*
         * Constructor for Student object. Takes a JSON Object or Dictionary and unpacks student information.
         */
        if let name = studentJSONObject["name"], let email = studentJSONObject["email"], let id = studentJSONObject["id"] {
            self.name = name
            self.email = email
            self.id = id
        } else {
            self.name = "StudentName"
            self.email = "StudentEmail"
            self.id = "0"
        }
    }
}
