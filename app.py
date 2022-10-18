#! /usr/bin/python3
import sys
import os
import random

json = {
    'compileSdk': 32,
    'minSdk': 21,
    'targetSdk': 32,
    'implementations': ['androidx.appcompat:appcompat:1.4.1', 'com.google.android.material:material:1.4.0'],
    'package': 'com.aa.test',
    'permission': ['android.permission.READ_PRIVILEGED_PHONE_STATE'],
    'packageCount': 30,
    'activityCount': 3,
    'serverCount': 2,
    'otherCount': 10,
    'methodCount': 20
}

table = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
         'w', 'x', 'y', 'z']

methods = [
    '''
    public void %s() {
        long now = System.currentTimeMillis();
        if (System.currentTimeMillis() < now) {
            System.out.println("Time travelling, woo hoo!");
            return;
        }

        if (System.currentTimeMillis() == now) {
            System.out.println("Time stood still!");
            return;
        }
        System.out.println("Ok, time still moving forward");
    }
    ''',
    '''
    public void %s(){
        for (int i=0;i<10;i++)
            System.out.println(i);
    }
    ''',
    '''
    public void %s(){
        try {
            throw new Exception("Failed");
        }catch (Exception e){
            e.printStackTrace();
        }
    }
    ''',
    '''
    public java.util.Date %s(){
        return new java.util.Date();
    }
    ''',
    '''
    public static void %s(String[] args){
        for (String s:args)
            System.out.println(s);
    }
    '''
]

layout_tab = [
    '''<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:orientation="vertical"
    android:layout_height="match_parent">

</LinearLayout>
    ''',
    '''<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:orientation="vertical"
    android:layout_height="match_parent">
    <TextView
        android:layout_width="match_parent"
        android:layout_height="match_parent"/>

</LinearLayout>   
    '''
]

packages = []
activities = []
servers = []
layouts = []


def create_app(dr):
    dr = os.path.join(dr, 'src')
    os.mkdir(dr)
    dr = os.path.join(dr, 'main')
    os.mkdir(dr)
    create_packages(dr)
    create_layout(dr)
    create_main(dr)


def create_layout(dr):
    if len(layouts) <= 0:
        return
    dr = os.path.join(dr, 'res')
    os.mkdir(dr)
    dr = os.path.join(dr, 'layout')
    os.mkdir(dr)
    for layout in layouts:
        with open(os.path.join(dr, '%s.xml' % layout), 'w') as f:
            f.write(layout_tab[random.randint(0, len(layout_tab) - 1)])


def create_packages(dr):
    dr = os.path.join(dr, 'java')
    os.mkdir(dr)
    package = json['package']
    for p in package.split('.'):
        dr = os.path.join(dr, p)
        os.mkdir(dr)
    for i in range(json['packageCount']):
        ss = next_string()
        while ss in packages:
            ss = next_string()
        packages.append(ss)
        create_java(os.path.join(dr, ss))


def create_java(dr):
    os.mkdir(dr)
    create_activity(dr)
    create_server(dr)
    create_other(dr)
    pass


def create_activity(dr):
    if 'activityCount' not in json:
        return
    acs = []
    for i in range(json['activityCount']):
        ss = next_string()
        while ss in acs:
            ss = next_string()
        layouts.append('activity_%s' % ss.lower())
        ss = ss.capitalize()
        ss = ss + 'Activity'
        create_activity_java(os.path.join(dr, '%s.java' % ss), ss[:-8])


def create_activity_java(dr, name):
    with open(dr, 'w') as f:
        package_name = dr.split('java/')[1]
        package_name = package_name[:package_name.rindex('/')]
        package_name = '.'.join(package_name.split('/'))
        activities.append("%s.%sActivity" % (package_name, name))
        f.write('''package %s;

import android.app.Activity;
import android.os.Bundle;

import androidx.annotation.Nullable;

import %s.R;


public class %sActivity extends Activity {
    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_%s);
    }
        ''' % (package_name, json['package'], name, name.lower()))
        add_method(f)
        f.write('}\n')
    pass


def create_server(dr):
    if 'serverCount' not in json:
        return
    acs = []
    for i in range(json['serverCount']):
        ss = next_string()
        while ss in acs:
            ss = next_string()
        ss = ss.capitalize()
        ss = ss + 'Service'
        create_server_java(os.path.join(dr, '%s.java' % ss), ss[:-7])


def create_server_java(dr, name):
    with open(dr, 'w') as f:
        package_name = dr.split('java/')[1]
        package_name = package_name[:package_name.rindex('/')]
        package_name = '.'.join(package_name.split('/'))
        servers.append("%s.%sServer" % (package_name, name))
        f.write('''package %s;

import android.app.Service;
import android.content.Intent;
import android.os.IBinder;

import androidx.annotation.Nullable;

public class %sService extends Service {
    @Override
    public void onCreate() {
        super.onCreate();
    }

    @Nullable
    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }
        ''' % (package_name, name))
        add_method(f)
        f.write('}\n')


def create_other(dr):
    pass
    if 'otherCount' not in json:
        return
    acs = []
    for i in range(json['otherCount']):
        ss = next_string()
        while ss in acs:
            ss = next_string()
        ss = ss.capitalize()
        create_other_java(os.path.join(dr, '%s.java' % ss), ss)


def create_other_java(dr, name):
    with open(dr, 'w') as f:
        package_name = dr.split('java/')[1]
        package_name = package_name[:package_name.rindex('/')]
        package_name = '.'.join(package_name.split('/'))
        f.write('package %s;\n\n' % package_name)
        f.write('public class %s{\n' % name)
        add_method(f)
        f.write('}\n')


def add_method(f):
    if 'methodCount' not in json:
        return
    meths = []
    for i in range(json['methodCount']):
        ss = next_string()
        while ss in meths:
            ss = next_string()
        meth = methods[random.randint(0, len(methods) - 1)]
        f.write(meth % ss)
        f.write('\n')


def next_string():
    length = random.randint(1, 20)
    ss = ''
    for i in range(length):
        index = random.randint(0, len(table) - 1)
        ss = ss + table[index]
    return ss


def create_main(dr):
    with open(os.path.join(dr, 'AndroidManifest.xml'), 'w') as f:
        f.write('<?xml version="1.0" encoding="utf-8"?>\n')
        f.write('<manifest xmlns:android="http://schemas.android.com/apk/res/android"\n')
        f.write('\tpackage="%s">\n' % json['package'])
        if 'permission' in json:
            for permission in json['permission']:
                f.write('\t<uses-permission android:name="%s" />\n' % permission)
        f.write('\t<application>\n')
        if activities:
            for activity in activities:
                f.write('\t\t<activity android:name="%s"\n' % activity)
                f.write('\t\t\tandroid:exported="false"/>\n')
        if servers:
            for server in servers:
                f.write('\t\t<service android:name="%s"\n' % server)
                f.write('\t\t\tandroid:exported="false"/>\n')
        f.write('\t</application>\n')
        f.write('</manifest>')


def clear(dr):
    if os.path.isfile(dr):
        os.remove(dr)
        return
    for f in os.listdir(dr):
        clear(os.path.join(dr, f))
    os.rmdir(dr)


def create_gradle(dr):
    with open(os.path.join(dr, 'build.gradle'), 'w') as f:
        f.write('plugins{\n\tid "com.android.library"\n}\n')
        f.write('android{\n\tcompileSdk %s\n\tdefaultConfig{\n\t\tminSdk %s\n\t\ttargetSdk %s\n\t}\n}' % (
            json['compileSdk'], json['minSdk'], json['targetSdk']))
        f.write('\ndependencies{\n')
        if 'implementations' in json:
            for implementation in json['implementations']:
                f.write('\timplementation "%s"\n' % implementation)
        f.write('}')


if __name__ == '__main__':
    app = sys.argv[1]
    print("项目输出地址:%s" % app)
    if not os.path.exists(app):
        os.makedirs(app)
    else:
        clear(app)
        os.makedirs(app)
    create_gradle(app)
    create_app(app)
