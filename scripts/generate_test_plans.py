#!/usr/bin/env python3
"""Generate the four built-in-component JMeter plans used by HW05."""

from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "test-plans"
STUDENT_ID = "23127373"  # HUMAN REVIEW: confirm before submission.
RUN_DATE = "20260814"


def string_prop(parent: ET.Element, name: str, value: str = "") -> ET.Element:
    node = ET.SubElement(parent, "stringProp", {"name": name})
    node.text = value
    return node


def bool_prop(parent: ET.Element, name: str, value: bool) -> ET.Element:
    node = ET.SubElement(parent, "boolProp", {"name": name})
    node.text = str(value).lower()
    return node


def int_prop(parent: ET.Element, name: str, value: int) -> ET.Element:
    node = ET.SubElement(parent, "intProp", {"name": name})
    node.text = str(value)
    return node


def pair(parent_tree: ET.Element, element: ET.Element) -> ET.Element:
    parent_tree.append(element)
    return ET.SubElement(parent_tree, "hashTree")


def test_plan(name: str, comment: str) -> tuple[ET.ElementTree, ET.Element]:
    root = ET.Element(
        "jmeterTestPlan",
        {"version": "1.2", "properties": "5.0", "jmeter": "5.6.3"},
    )
    root_tree = ET.SubElement(root, "hashTree")
    plan = ET.Element(
        "TestPlan",
        {
            "guiclass": "TestPlanGui",
            "testclass": "TestPlan",
            "testname": name,
            "enabled": "true",
        },
    )
    string_prop(plan, "TestPlan.comments", comment)
    bool_prop(plan, "TestPlan.functional_mode", False)
    bool_prop(plan, "TestPlan.serialize_threadgroups", False)
    args = ET.SubElement(
        plan,
        "elementProp",
        {
            "name": "TestPlan.user_defined_variables",
            "elementType": "Arguments",
            "guiclass": "ArgumentsPanel",
            "testclass": "Arguments",
            "testname": "User Defined Variables",
            "enabled": "true",
        },
    )
    ET.SubElement(args, "collectionProp", {"name": "Arguments.arguments"})
    string_prop(plan, "TestPlan.user_define_classpath", "")
    plan_tree = pair(root_tree, plan)
    return ET.ElementTree(root), plan_tree


def add_csv(plan_tree: ET.Element) -> None:
    csv = ET.Element(
        "CSVDataSet",
        {
            "guiclass": "TestBeanGUI",
            "testclass": "CSVDataSet",
            "testname": "CSV seed data: name, password, domain",
            "enabled": "true",
        },
    )
    string_prop(csv, "delimiter", ",")
    string_prop(csv, "fileEncoding", "UTF-8")
    string_prop(csv, "filename", "${__P(csv_file,data/users.csv)}")
    bool_prop(csv, "ignoreFirstLine", True)
    bool_prop(csv, "quotedData", False)
    bool_prop(csv, "recycle", True)
    string_prop(csv, "shareMode", "shareMode.all")
    bool_prop(csv, "stopThread", False)
    string_prop(csv, "variableNames", "name,password,domain")
    pair(plan_tree, csv)


def add_http_defaults(plan_tree: ET.Element) -> None:
    defaults = ET.Element(
        "ConfigTestElement",
        {
            "guiclass": "HttpDefaultsGui",
            "testclass": "ConfigTestElement",
            "testname": "HTTP Request Defaults",
            "enabled": "true",
        },
    )
    args = ET.SubElement(
        defaults,
        "elementProp",
        {
            "name": "HTTPsampler.Arguments",
            "elementType": "Arguments",
            "guiclass": "HTTPArgumentsPanel",
            "testclass": "Arguments",
            "testname": "User Defined Variables",
            "enabled": "true",
        },
    )
    ET.SubElement(args, "collectionProp", {"name": "Arguments.arguments"})
    string_prop(defaults, "HTTPSampler.domain", "${__P(host,localhost)}")
    string_prop(defaults, "HTTPSampler.port", "${__P(port,3000)}")
    string_prop(defaults, "HTTPSampler.protocol", "http")
    string_prop(defaults, "HTTPSampler.contentEncoding", "UTF-8")
    string_prop(defaults, "HTTPSampler.connect_timeout", "5000")
    string_prop(defaults, "HTTPSampler.response_timeout", "10000")
    pair(plan_tree, defaults)

    headers = ET.Element(
        "HeaderManager",
        {
            "guiclass": "HeaderPanel",
            "testclass": "HeaderManager",
            "testname": "HTTP Header Manager",
            "enabled": "true",
        },
    )
    collection = ET.SubElement(headers, "collectionProp", {"name": "HeaderManager.headers"})
    for header_name, header_value in (
        ("Content-Type", "application/json"),
        ("Accept", "application/json"),
        ("Authorization", "Bearer ${__P(admin_jwt,NOT_SET)}"),
    ):
        item = ET.SubElement(
            collection,
            "elementProp",
            {"name": header_name, "elementType": "Header"},
        )
        string_prop(item, "Header.name", header_name)
        string_prop(item, "Header.value", header_value)
    pair(plan_tree, headers)


def jsr223_element(testclass: str, testname: str, script: str) -> ET.Element:
    gui = "TestBeanGUI"
    node = ET.Element(
        testclass,
        {
            "guiclass": gui,
            "testclass": testclass,
            "testname": testname,
            "enabled": "true",
        },
    )
    string_prop(node, "cacheKey", "true")
    string_prop(node, "filename", "")
    string_prop(node, "parameters", "")
    string_prop(node, "script", script.strip())
    string_prop(node, "scriptLanguage", "groovy")
    return node


def http_request(name: str, method: str, path: str, body: str = "") -> ET.Element:
    sampler = ET.Element(
        "HTTPSamplerProxy",
        {
            "guiclass": "HttpTestSampleGui",
            "testclass": "HTTPSamplerProxy",
            "testname": name,
            "enabled": "true",
        },
    )
    args = ET.SubElement(
        sampler,
        "elementProp",
        {
            "name": "HTTPsampler.Arguments",
            "elementType": "Arguments",
            "guiclass": "HTTPArgumentsPanel",
            "testclass": "Arguments",
            "testname": "User Defined Variables",
            "enabled": "true",
        },
    )
    collection = ET.SubElement(args, "collectionProp", {"name": "Arguments.arguments"})
    if body:
        arg = ET.SubElement(collection, "elementProp", {"name": "", "elementType": "HTTPArgument"})
        bool_prop(arg, "HTTPArgument.always_encode", False)
        string_prop(arg, "Argument.value", body)
        string_prop(arg, "Argument.metadata", "=")
    string_prop(sampler, "HTTPSampler.path", path)
    string_prop(sampler, "HTTPSampler.method", method)
    bool_prop(sampler, "HTTPSampler.follow_redirects", True)
    bool_prop(sampler, "HTTPSampler.auto_redirects", False)
    bool_prop(sampler, "HTTPSampler.use_keepalive", True)
    bool_prop(sampler, "HTTPSampler.DO_MULTIPART_POST", False)
    string_prop(sampler, "HTTPSampler.embedded_url_re", "")
    string_prop(sampler, "HTTPSampler.implementation", "HttpClient4")
    bool_prop(sampler, "HTTPSampler.postBodyRaw", bool(body))
    return sampler


PREPROCESSOR = r"""
import java.util.UUID
vars.put('registered_id', 'NOT_FOUND')
def domain = vars.get('domain') ?: 'loadtest.local'
def scenario = (props.get('scenario') ?: 'unknown').toString().toLowerCase()
vars.put('test_email', "${scenario}-${UUID.randomUUID()}@${domain}")
"""

REGISTER_ASSERTION = r"""
import groovy.json.JsonSlurper
if (prev.getResponseCode() != '200') {
    AssertionResult.setFailure(true)
    AssertionResult.setFailureMessage('Expected HTTP 200, received ' + prev.getResponseCode())
    return
}
try {
    def json = new JsonSlurper().parseText(prev.getResponseDataAsString())
    if (!(json.id instanceof Number) || json.id.longValue() <= 0) {
        AssertionResult.setFailure(true)
        AssertionResult.setFailureMessage('Registration response lacks a positive numeric id')
    }
} catch (Exception ex) {
    AssertionResult.setFailure(true)
    AssertionResult.setFailureMessage('Registration response is not valid JSON: ' + ex.message)
}
"""

GET_ASSERTION = r"""
import groovy.json.JsonSlurper
if (prev.getResponseCode() != '200') {
    AssertionResult.setFailure(true)
    AssertionResult.setFailureMessage('Expected HTTP 200, received ' + prev.getResponseCode())
    return
}
try {
    def rows = new JsonSlurper().parseText(prev.getResponseDataAsString())
    def wantedId = vars.get('registered_id')
    def wantedEmail = vars.get('test_email')
    def match = rows instanceof List && rows.any {
        it.id?.toString() == wantedId && it.email?.toString() == wantedEmail
    }
    if (!match) {
        AssertionResult.setFailure(true)
        AssertionResult.setFailureMessage('Created user was not found by exact id and email')
    }
} catch (Exception ex) {
    AssertionResult.setFailure(true)
    AssertionResult.setFailureMessage('User-list response is not valid JSON: ' + ex.message)
}
"""

DELETE_ASSERTION = r"""
if (prev.getResponseCode() != '200') {
    AssertionResult.setFailure(true)
    AssertionResult.setFailureMessage('Expected HTTP 200, received ' + prev.getResponseCode())
} else if (!prev.getResponseDataAsString().contains('User deleted')) {
    AssertionResult.setFailure(true)
    AssertionResult.setFailureMessage('Delete acknowledgement is missing')
}
"""


def add_workflow(thread_tree: ET.Element, think_base: str, think_range: str) -> None:
    tx = ET.Element(
        "TransactionController",
        {
            "guiclass": "TransactionControllerGui",
            "testclass": "TransactionController",
            "testname": "TC_Account_Lifecycle",
            "enabled": "true",
        },
    )
    bool_prop(tx, "TransactionController.includeTimers", False)
    bool_prop(tx, "TransactionController.parent", False)
    tx_tree = pair(thread_tree, tx)

    register = http_request(
        "01_POST_register",
        "POST",
        "/api/register",
        '{"name":"${name}","email":"${test_email}","password":"${password}"}',
    )
    register_tree = pair(tx_tree, register)
    pair(register_tree, jsr223_element("JSR223PreProcessor", "Generate UUID email", PREPROCESSOR))

    extractor = ET.Element(
        "JSONPostProcessor",
        {
            "guiclass": "JSONPostProcessorGui",
            "testclass": "JSONPostProcessor",
            "testname": "Extract registered user id",
            "enabled": "true",
        },
    )
    string_prop(extractor, "JSONPostProcessor.referenceNames", "registered_id")
    string_prop(extractor, "JSONPostProcessor.jsonPathExprs", "$.id")
    string_prop(extractor, "JSONPostProcessor.match_numbers", "1")
    string_prop(extractor, "JSONPostProcessor.defaultValues", "NOT_FOUND")
    pair(register_tree, extractor)
    pair(register_tree, jsr223_element("JSR223Assertion", "Assert registration response", REGISTER_ASSERTION))

    condition = ET.Element(
        "IfController",
        {
            "guiclass": "IfControllerPanel",
            "testclass": "IfController",
            "testname": "If registration returned id: verify and clean up",
            "enabled": "true",
        },
    )
    string_prop(condition, "IfController.condition", "${__groovy(vars.get('registered_id') != 'NOT_FOUND')}")
    bool_prop(condition, "IfController.evaluateAll", False)
    if_tree = pair(tx_tree, condition)

    get_users = http_request("02_GET_admin_users", "GET", "/api/admin/users")
    get_tree = pair(if_tree, get_users)
    pair(get_tree, jsr223_element("JSR223Assertion", "Assert exact user id and email", GET_ASSERTION))

    delete_user = http_request(
        "03_DELETE_registered_user",
        "DELETE",
        "/api/admin/users/${registered_id}",
    )
    delete_tree = pair(if_tree, delete_user)
    pair(delete_tree, jsr223_element("JSR223Assertion", "Assert delete acknowledgement", DELETE_ASSERTION))

    action = ET.Element(
        "TestAction",
        {
            "guiclass": "TestActionGui",
            "testclass": "TestAction",
            "testname": "Think time between lifecycle iterations",
            "enabled": "true",
        },
    )
    int_prop(action, "ActionProcessor.action", 1)
    int_prop(action, "ActionProcessor.target", 0)
    string_prop(action, "ActionProcessor.duration", "0")
    action_tree = pair(thread_tree, action)
    timer = ET.Element(
        "UniformRandomTimer",
        {
            "guiclass": "UniformRandomTimerGui",
            "testclass": "UniformRandomTimer",
            "testname": "Scenario pacing",
            "enabled": "true",
        },
    )
    string_prop(timer, "ConstantTimer.delay", think_base)
    string_prop(timer, "RandomTimer.range", think_range)
    pair(action_tree, timer)


def add_thread_group(
    plan_tree: ET.Element,
    name: str,
    threads: str,
    ramp: str,
    delay: str,
    duration: str,
    think_base: str,
    think_range: str,
) -> None:
    group = ET.Element(
        "ThreadGroup",
        {
            "guiclass": "ThreadGroupGui",
            "testclass": "ThreadGroup",
            "testname": name,
            "enabled": "true",
        },
    )
    string_prop(group, "ThreadGroup.on_sample_error", "continue")
    loop = ET.SubElement(
        group,
        "elementProp",
        {
            "name": "ThreadGroup.main_controller",
            "elementType": "LoopController",
            "guiclass": "LoopControlPanel",
            "testclass": "LoopController",
            "testname": "Loop Controller",
            "enabled": "true",
        },
    )
    bool_prop(loop, "LoopController.continue_forever", True)
    string_prop(loop, "LoopController.loops", "-1")
    string_prop(group, "ThreadGroup.num_threads", threads)
    string_prop(group, "ThreadGroup.ramp_time", ramp)
    bool_prop(group, "ThreadGroup.scheduler", True)
    string_prop(group, "ThreadGroup.duration", duration)
    string_prop(group, "ThreadGroup.delay", delay)
    bool_prop(group, "ThreadGroup.same_user_on_next_iteration", True)
    thread_tree = pair(plan_tree, group)
    add_workflow(thread_tree, think_base, think_range)


def add_listener(plan_tree: ET.Element, gui: str, name: str, default_file: str) -> None:
    listener = ET.Element(
        "ResultCollector",
        {
            "guiclass": gui,
            "testclass": "ResultCollector",
            "testname": name,
            "enabled": "true",
        },
    )
    bool_prop(listener, "ResultCollector.error_logging", False)
    obj = ET.SubElement(listener, "objProp")
    n = ET.SubElement(obj, "name")
    n.text = "saveConfig"
    value = ET.SubElement(obj, "value", {"class": "SampleSaveConfiguration"})
    for field, enabled in (
        ("time", True), ("latency", True), ("timestamp", True), ("success", True),
        ("label", True), ("code", True), ("message", True), ("threadName", True),
        ("dataType", True), ("encoding", False), ("assertions", True),
        ("subresults", True), ("responseData", False), ("samplerData", False),
        ("xml", False), ("fieldNames", True), ("responseHeaders", False),
        ("requestHeaders", False), ("responseDataOnError", False),
        ("saveAssertionResultsFailureMessage", True), ("bytes", True),
        ("sentBytes", True), ("url", True), ("threadCounts", True),
        ("idleTime", True), ("connectTime", True),
    ):
        child = ET.SubElement(value, field)
        child.text = str(enabled).lower()
    ar = ET.SubElement(value, "assertionsResultsToSave")
    ar.text = "0"
    string_prop(listener, "filename", "${__P(listener_file," + default_file + ")}")
    pair(plan_tree, listener)


def indent(tree: ET.ElementTree) -> None:
    ET.indent(tree, space="  ")


def write_plan(scenario: str, groups: list[dict[str, str]], listener: tuple[str, str]) -> Path:
    filename = f"{STUDENT_ID}_{scenario}_{RUN_DATE}.jmx"
    tree, plan_tree = test_plan(
        filename.removesuffix(".jmx"),
        "Same account-lifecycle workflow in every scenario: register -> exact admin read verification -> delete cleanup.",
    )
    add_csv(plan_tree)
    add_http_defaults(plan_tree)
    for group in groups:
        add_thread_group(plan_tree, **group)
    gui, label = listener
    add_listener(plan_tree, gui, label, f"results/listeners/{scenario.lower()}-listener.jtl")
    indent(tree)
    target = OUT / filename
    tree.write(target, encoding="utf-8", xml_declaration=True)
    return target


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    plans = []
    plans.append(
        write_plan(
            "Load",
            [{
                "name": "Load steady state",
                "threads": "${__P(load_threads,15)}",
                "ramp": "${__P(load_ramp,30)}",
                "delay": "0",
                "duration": "${__P(load_duration,300)}",
                "think_base": "${__P(load_think_base,300)}",
                "think_range": "${__P(load_think_range,700)}",
            }],
            ("SummaryReport", "Summary Report - Load"),
        )
    )
    stress_groups = []
    for index, (delay, duration) in enumerate(((0, 480), (120, 360), (240, 240), (360, 120)), start=1):
        stress_groups.append({
            "name": f"Stress increment {index}",
            "threads": "${__P(stress_step_threads,10)}",
            "ramp": "${__P(stress_step_ramp,10)}",
            "delay": f"${{__P(stress_delay_{index},{delay})}}",
            "duration": f"${{__P(stress_duration_{index},{duration})}}",
            "think_base": "${__P(stress_think_base,50)}",
            "think_range": "${__P(stress_think_range,150)}",
        })
    plans.append(write_plan("Stress", stress_groups, ("StatVisualizer", "Aggregate Report - Stress")))
    plans.append(
        write_plan(
            "Spike",
            [
                {
                    "name": "Spike baseline and recovery",
                    "threads": "${__P(spike_baseline_threads,10)}",
                    "ramp": "${__P(spike_baseline_ramp,20)}",
                    "delay": "0",
                    "duration": "${__P(spike_baseline_duration,420)}",
                    "think_base": "${__P(spike_think_base,100)}",
                    "think_range": "${__P(spike_think_range,200)}",
                },
                {
                    "name": "Spike increment",
                    "threads": "${__P(spike_extra_threads,40)}",
                    "ramp": "${__P(spike_ramp,5)}",
                    "delay": "${__P(spike_delay,120)}",
                    "duration": "${__P(spike_duration,60)}",
                    "think_base": "${__P(spike_think_base,100)}",
                    "think_range": "${__P(spike_think_range,200)}",
                },
            ],
            ("ViewResultsFullVisualizer", "View Results Tree - Spike evidence only"),
        )
    )
    plans.append(
        write_plan(
            "Soak",
            [{
                "name": "Soak sustained load",
                "threads": "${__P(soak_threads,10)}",
                "ramp": "${__P(soak_ramp,60)}",
                "delay": "0",
                "duration": "${__P(soak_duration,900)}",
                "think_base": "${__P(soak_think_base,300)}",
                "think_range": "${__P(soak_think_range,700)}",
            }],
            ("StatVisualizer", "Aggregate Report - Soak supporting view"),
        )
    )
    for path in plans:
        print(path.relative_to(ROOT))


if __name__ == "__main__":
    main()
