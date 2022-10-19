#! /usr/bin/python3
import sys
import os
import random
import json as js

json = {
}

word_table = []

fields = []

key = ['private', 'protected', 'public', 'default', 'abstract', 'class', 'extends',
       'final', 'implements', 'interface', 'native', 'new', 'static', 'strictfp',
       'synchronized', 'transient', 'volatile', 'break', 'case', 'continue', 'do',
       'else', 'for', 'if', 'instanceof', 'return', 'switch', 'while', 'assert', 'catch',
       'finally', 'throw', 'throws', 'try', 'import', 'package', 'boolean', 'byte',
       'char', 'double', 'float', 'int', 'long', 'short', 'super', 'this', 'void',
       'goto', 'const', 'Activity', 'Service']

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
    create_res(dr)
    create_main(dr)


def create_res(dr):
    dr = os.path.join(dr, 'res')
    os.mkdir(dr)
    create_layout(dr)
    create_values(dr)


def create_values(dr):
    dr = os.path.join(dr, 'values')
    os.mkdir(dr)
    create_color(dr)
    create_string(dr)


color_table = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']


def create_color_():
    ss = color_table[random.randint(0, len(color_table) - 1)]
    for i in range(7):
        ss = ss + color_table[random.randint(0, len(color_table) - 1)]
    return ss


def create_color(dr):
    if 'colorCount' not in json:
        return
    with open(os.path.join(dr, 'colors.xml'), 'w') as f:
        f.write('<?xml version="1.0" encoding="utf-8"?>\n<resources>\n')
        colors = []
        for i in range(json['colorCount']):
            ss = next_string()
            while ss in colors:
                ss = next_string()
            colors.append(ss)
            ss = name_to_layout(ss)
            f.write('<color name="%s">#%s</color>\n' % (ss, create_color_()))
        f.write('</resources>')
    pass


def create_string(dr):
    if 'stringCount' not in json:
        return
    with open(os.path.join(dr, 'strings.xml'), 'w') as f:
        f.write('<?xml version="1.0" encoding="utf-8"?>\n<resources>\n')
        strings = []
        for i in range(json['stringCount']):
            ss = next_string()
            while ss in strings:
                ss = next_string()
            strings.append(ss)
            ss = name_to_layout(ss)
            f.write('<string name="%s">%s</string>\n' % (ss, ss.replace('_', ' ')))
        f.write('</resources>')


def create_layout(dr):
    if len(layouts) <= 0:
        return
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
        while ss in packages or ss in key:
            ss = next_string()
        ss = str(ss).lower()
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
        while ss in acs or ss in key:
            ss = next_string()
        ss = str(ss[0:1]).upper() + ss[1:]
        if not str(ss).endswith('Activity'):
            ss = ss + 'Activity'
        create_activity_java(os.path.join(dr, '%s.java' % ss), ss[:-8])


def name_to_layout(name):
    ss = str(name[0:1]).lower()
    for i in name[1:]:
        if str(i).upper() == i:
            ss = ss + '_' + str(i).lower()
        else:
            ss = ss + i
    return ss


def create_activity_java(dr, name):
    layout_name = name_to_layout(name)
    layouts.append('activity_%s' % layout_name)
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


public class %sActivity extends Activity {''' % (package_name, json['package'], name))
        add_field(f)
        f.write('''    
    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_%s);
    }
            ''' % (layout_name))
        add_method(f)
        f.write('}\n')
    pass


def create_server(dr):
    if 'serverCount' not in json:
        return
    acs = []
    for i in range(json['serverCount']):
        ss = next_string()
        while ss in acs and ss in key:
            ss = next_string()
        ss = str(ss[0:1]).upper() + ss[1:]
        if not str(ss).endswith('Service'):
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

public class %sService extends Service {''' % (package_name, name))
        add_field(f)
        f.write('''
    @Override
    public void onCreate() {
        super.onCreate();
    }

    @Nullable
    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }
        ''')
        add_method(f)
        f.write('}\n')


def create_other(dr):
    pass
    if 'otherCount' not in json:
        return
    acs = []
    for i in range(json['otherCount']):
        ss = next_string()
        while ss in acs and ss in key:
            ss = next_string()
        ss = str(ss[0:1]).upper() + ss[1:]
        create_other_java(os.path.join(dr, '%s.java' % ss), ss)


def create_other_java(dr, name):
    with open(dr, 'w') as f:
        package_name = dr.split('java/')[1]
        package_name = package_name[:package_name.rindex('/')]
        package_name = '.'.join(package_name.split('/'))
        f.write('package %s;\n\n' % package_name)
        f.write('public class %s{\n' % name)
        add_field(f)
        add_method(f)
        f.write('}\n')


def add_method(f):
    if 'methodCount' not in json:
        return
    meths = []
    for i in range(json['methodCount']):
        ss = next_string()
        while ss in meths and ss in key:
            ss = next_string()
        meths.append(ss)
        meth = methods[random.randint(0, len(methods) - 1)]
        f.write(meth % ss)
        f.write('\n')


def add_field(f):
    if 'fieldCount' not in json:
        return
    fiels = []
    for i in range(json['fieldCount']):
        ss = next_string()
        while ss in fiels and ss in key:
            ss = next_string()
        fiels.append(ss)
        meth = fields[random.randint(0, len(fields) - 1)]
        f.write('\n\tprivate %s %s;' % (meth, ss))
        f.write('\n')


def next_string():
    length = random.randint(1, 3)
    index = random.randint(0, len(word_table) - 1)
    ss = word_table[index]
    if length < 2:
        return ss
    for i in range(length - 1):
        index = random.randint(0, len(word_table) - 1)
        ss = ss + str(word_table[index]).capitalize()
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


def init_word():
    with open('words', 'r') as f:
        for line in f.readlines():
            word_table.append(line.replace('\n', ''))


def init_field():
    with open('fields', 'r') as f:
        for line in f.readlines():
            fields.append(line.replace('\n', ''))


if __name__ == '__main__':
    app = sys.argv[1]
    print("项目输出地址:%s" % app)
    with open('config.json', 'r') as f:
        json = js.load(f)
    init_word()
    init_field()
    if not os.path.exists(app):
        os.makedirs(app)
    else:
        clear(app)
        os.makedirs(app)
    create_gradle(app)
    create_app(app)
