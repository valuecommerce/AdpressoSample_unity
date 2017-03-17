//
//  AdLantisConversion.h
//  adlantis_iphone_sdk
//
//  Created on 10/3/12.
//  Copyright (c) 2014 Atlantis Inc. All rights reserved.
//

#import <Foundation/Foundation.h>

__attribute__ ((deprecated))
@interface AdLantisConversion : NSObject

+ (instancetype)conversionWithTag:(NSString*)tag;

+ (void)sendConversionWithTag:(NSString*)tag;

- (instancetype)initWithTag:(NSString*)tag;

- (void)send;

- (NSString*)tag;

@end
#pragma clang diagnostic push
#pragma clang diagnostic ignored "-Wdeprecated"
@interface AdLantisConversionTest : AdLantisConversion
#pragma clang diagnostic pop

@end
