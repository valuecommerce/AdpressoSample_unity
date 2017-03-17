//
//  AdpressoAdManager.h
//  AdLantis iOS SDK
//
//  Copyright 2009-2014 Atlantiss.jp. All rights reserved.
//  Copyright 2016 valuecommerce All rights reserved.
//

#import <Foundation/Foundation.h>

///////////////////////////////////////////////////////////////////////////////////////////////////
@interface AdpressoAdManager : NSObject

+ (instancetype)sharedManager;

+ (NSString*)versionString;                                       // AdLantis SDK version
+ (NSString*)build;                                               // AdLantis SDK build
@property (nonatomic,readonly,copy) NSString *fullVersionString;  // Complete version information in one line

@end
