//
//  Location.swift
//  AttendanceApplication
//

import Foundation

class Location {
    
    // MARK: Public properties

    var roomNumber: String! // a.k.a. beacon name
    var description: String!
    var zoneId: String!
    var timestamp: String!
    
    // MARK: Init
    
    init(locationJSONObject: [String: String]) {
        if let roomNumber = locationJSONObject["room_number"], let description = locationJSONObject["description"], let timestamp = locationJSONObject["timestamp"], let zoneId = locationJSONObject["zone_id"] {
            self.roomNumber = roomNumber
            self.description = description
            self.timestamp = timestamp
            self.zoneId = zoneId
        } else {
            self.roomNumber = "room_number"
            self.description = "description"
            self.timestamp = "timestamp"
            self.zoneId = "zoneId"
        }
    }
}
