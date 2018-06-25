//
//  Beacon.swift
//  AttendanceApplication
//

import Foundation

class Beacon {
    
    // MARK: Public Properties
    
    var roomNumber: String!
    var description: String!
    var id: String!
    var zoneName: String!
    
    // MARK: Init
    
    init(beaconJSONObject: [String: String]) {
        if let roomNumber = beaconJSONObject["room_number"], let description = beaconJSONObject["description"], let id = beaconJSONObject["id"], let zoneName = beaconJSONObject["zone_name"]  {
            self.roomNumber = roomNumber
            self.description = description
            self.id = id
            self.zoneName = zoneName
        } else {
            self.roomNumber = "roomNumber"
            self.description = "description"
            self.id = "id"
            self.zoneName = "zoneName"
        }
    }
}
