plugins {
    id("com.android.application")
}

android {
    namespace = "com.example.torchandroid"
    compileSdk = 34

    defaultConfig {
        applicationId = "com.example.torchandroid"
        minSdk = 25
        targetSdk = 34
        versionCode = 1
        versionName = "1.0"

        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_1_8
        targetCompatibility = JavaVersion.VERSION_1_8
    }
}

dependencies {

    implementation("org.pytorch:pytorch_android_lite:1.10.0")
    implementation("org.pytorch:pytorch_android_torchvision_lite:1.10.0")
    implementation("androidx.appcompat:appcompat:1.6.1")
    implementation("com.google.android.material:material:1.9.0")
    implementation("androidx.constraintlayout:constraintlayout:2.1.4")
    testImplementation("junit:junit:4.13.2")
    androidTestImplementation("androidx.test.ext:junit:1.1.5")
    androidTestImplementation("androidx.test.espresso:espresso-core:3.5.1")

    val camerx_version = "1.1.0-beta01"
    implementation("androidx.camera:camera-core:${camerx_version}")
    implementation("androidx.camera:camera-camera2:${camerx_version}")
    implementation("androidx.camera:camera-lifecycle:${camerx_version}")
    implementation("androidx.camera:camera-video:${camerx_version}")
    implementation("androidx.camera:camera-view:${camerx_version}")
    implementation("androidx.camera:camera-extensions:${camerx_version}")
}